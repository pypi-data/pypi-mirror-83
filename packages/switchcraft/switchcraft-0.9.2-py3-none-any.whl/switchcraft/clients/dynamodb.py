"""DynamoDB Client.

Provides a client for DynamoDB.
"""

import logging

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class DynamoDBClient:

    def __init__(self, table_name: str, hash_key: str = None):
        self.dynamodb = boto3.resource('dynamodb')

        try:
            self.hash_key = hash_key
            self.table = self.dynamodb.Table(table_name)
        except ClientError as err:
            log.error(err)
            raise

    def get_item(
        self,
        partition_key_value: str,
        consistent_read: bool = True
    ) -> dict:
        log.debug(
            f'Querying table "{self.table.table_name}" for item with '
            f'hash value {partition_key_value}'
        )
        try:
            return self.table.get_item(
                Key={self.hash_key: partition_key_value},
                ConsistentRead=consistent_read
            )
        except ClientError as err:
            log.error(err)
            raise
