import boto3
from botocore.client import Config


class AwsHelper:
    def get_client(self, name, aws_region=None):
        config = Config(
            retries=dict(
                max_attempts=30
            )
        )
        if aws_region:
            return boto3.client(name, region_name=aws_region, config=config)
        else:
            return boto3.client(name, config=config)

    def get_resource(self, name, aws_region=None):
        config = Config(
            retries=dict(
                max_attempts=30
            )
        )

        if aws_region:
            return boto3.resource(name, region_name=aws_region, config=config)
        else:
            return boto3.resource(name, config=config)
