"""
This file contains multiple functions that offers
the functionality to interact with S3
"""
import logging
import re
import typing

import boto3
import botocore


logger = logging.getLogger(__name__)


def parse_s3(s3_path: str) -> typing.Tuple[str]:
    """parse the S3 path to return bucket name and the S3 path

    Args:
        s3_path (str): full S3 path as input

    Returns:
        s3bucket (str): S3 bucket name
        s3_path (str): S3 path

    """
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3_path)
    s3bucket = m.group(1)
    s3_path = m.group(2)

    return s3bucket, s3_path


def upload_file_to_s3(local_path: str, s3_path: str) -> None:
    """Upload the file from the local path to s3

    Args:
        local_path (str): the path to the local data
        s3_path (str): the s3 path that the data will be uploaded to

    Returns:
        None

    """
    s3bucket, s3_just_path = parse_s3(s3_path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error(
            "Please provide AWS credentials via AWS_ACCESS_KEY_ID "
            "and AWS_SECRET_ACCESS_KEY env variables."
        )
    else:
        logger.info("Data uploaded from %s to %s", local_path, s3_path)


def download_file_from_s3(local_path: str, s3_path: str) -> None:
    """Download the file from s3 to the local path

    Args:
        local_path (str): the path to the local data
        s3_path (str): the s3 path that the data will be downloaded from

    Returns:
        None

    """
    s3bucket, s3_just_path = parse_s3(s3_path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.download_file(s3_just_path, local_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error(
            "Please provide AWS credentials via AWS_ACCESS_KEY_ID "
            "and AWS_SECRET_ACCESS_KEY env variables."
        )
    else:
        logger.info("Data downloaded from %s to %s", s3_path, local_path)
