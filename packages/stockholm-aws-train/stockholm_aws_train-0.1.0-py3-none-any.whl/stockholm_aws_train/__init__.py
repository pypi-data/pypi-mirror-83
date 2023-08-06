import os
import time
from typing import List, Dict

import requests
import boto3
from fabric import Connection
from plute.utils.logger import log


def get_this_instance_id():
    """
    Read the docs at
    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html
    """
    res = requests.get("http://169.254.169.254/latest/meta-data/instance-id")
    if res.status_code == 200:
        return res.text
    return None


def destroy_instance(instance_id):
    """
    Select all or instances performing a particular job
    spawned by this project and delete them.
    """
    ec2_client = boto3.client("ec2")
    instance_ids = [instance_id] if instance_id else []
    if instance_ids:
        time.sleep(60)
        ec2_client.terminate_instances(InstanceIds=instance_ids)


def spawn(image_id: str, job: str, count: int,
          instance_type: str = "t2.small",
          availability_zone: str = "ap-south-1a",
          security_groups: List[str] = None,
          tags: List[Dict] = None,
          key_name: str = ""):
    """
    Build one instance given some configuration.
    """
    if not security_groups:
        raise ValueError("security groups need to have a value")
    if not job:
        raise ValueError("Job needs to have a value")
    if not key_name:
        raise ValueError("key_name needs to have a value [Pem file]")

    default_tags = [{
        "ResourceType": "instance",
        "Tags": [{
            "Key": "Name",
            "Value": f"plute_{job}"
        }, {
            "Key": "project",
            "Value": "plute"
        }, {
            "Key": "job",
            "Value": job
        }]
    }]

    tags = tags or default_tags

    ec2 = boto3.client("ec2", region_name=availability_zone[:-1])
    response = ec2.run_instances(
        ImageId=image_id,
        MinCount=count,
        MaxCount=count,
        InstanceType=instance_type,
        Placement={
            "AvailabilityZone": availability_zone
        },
        SecurityGroupIds=security_groups,
        KeyName=key_name,
        TagSpecifications=tags
    )

    return [instance["InstanceId"] for instance in response["Instances"]]


def get_public_name(instance_ids, region_name="ap-south-1"):
    """
    Get public dns name to ssh into instance.
    """
    ec2 = boto3.client("ec2", region_name=region_name)
    response = ec2.describe_instances(InstanceIds=instance_ids)
    if not response:
        return None
    return [reservation["PublicDnsName"]
            for reservation in response["Reservations"][0]["Instances"]]


def generate_ec2_instance_id(lang, project):
    owner = os.environ["OWNER"]
    environment = "Production"
    team = "ml"
    purpose = "training_model_patch"
    tag_name = f"{owner}-{environment}-{team}-{project}-{purpose}"
    filter_object = [{
        "Name": "tag:Project",
        "Values": [project]
    }, {
        "Name": "tag:Owner",
        "Values": [owner]
    }, {
        "Name": "tag:Environment",
        "Values": [environment]
    }, {
        "Name": "tag:Team",
        "Values": [team]
    }, {
        "Name": "tag:Purpose",
        "Values": [purpose]
    }, {
        "Name": "tag:Name",
        "Values": [tag_name]
    }, {
        "Name": "tag:Lang",
        "Values": [lang]
    }, {
        "Name": "instance-state-name",
        "Values": ["running"]
    }]
    tags = [{
        "ResourceType": "instance",
        "Tags": [{
            "Key": "Name",
            "Value": tag_name
        }, {
            "Key": "Project",
            "Value": project
        }, {
            "Key": "Owner",
            "Value": owner
        }, {
            "Key": "Environment",
            "Value": environment
        }, {
            "Key": "Team",
            "Value": team
        }, {
            "Key": "Purpose",
            "Value": purpose
        }, {
            "Key": "Lang",
            "Value": lang
        }]
    }]
    return filter_object, tags


def check_instance_exists(instance_filers):
    ec2 = boto3.client("ec2", region_name="ap-south-1")
    response = ec2.describe_instances(Filters=instance_filers)
    return bool(response["Reservations"])


def initiate_training(host, keyfile, current_version, new_version, lang):
    retries = 0
    keys = {"key_filename": keyfile}
    try:
        with Connection(host=host, user="ubuntu", connect_kwargs=keys) as conn:
            print(conn)
            conn.run("tmux new -d -s training", hide=False)
            conn.run(
                "tmux send -t training.0"
                f" './scripts/retrain.sh {current_version} {new_version} {lang}'"
                " ENTER")
            return True
    except BlockingIOError:
        time.sleep(20)
        retries += 1
        if retries < 50:
            initiate_training(host, keyfile, current_version,
                              new_version, lang)
