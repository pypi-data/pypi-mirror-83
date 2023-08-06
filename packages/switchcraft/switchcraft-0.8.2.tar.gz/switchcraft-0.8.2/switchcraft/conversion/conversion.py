"""Conversion.

Utility functions that assist with common (or helpful) conversions.
"""
import logging
import re
from ..data_classes.arn import ARN

log = logging.getLogger(__name__)


class MalformedArnError(Exception):
    def __init__(self, arn) -> None:
        self.arn = arn

    def __str__(self) -> str:
        return f'arn: {self.arn}'


def parse_arn(arn: str) -> ARN:
    """Given an ARN, this function returns its elements as a Python dictionary"""

    if not arn.startswith('arn:'):
        raise MalformedArnError(arn)

    elements = arn.split(':', 5)

    arn = ARN(
        arn=elements[0],
        partition=elements[1],
        service=elements[2],
        region=elements[3],
        account=elements[5],
        resourceType=None
    )

    if '/' in arn['resource']:
        arn['resource_type'], arn['resource'] = arn['resource'].split('/', 1)  # NOQA
    elif ':' in arn['resource']:
        arn['resource_type'], arn['resource'] = arn['resource'].split(':', 1)  # NOQA
    return arn


def underscore_to_camelcase(name: str) -> str:
    """Converts a string (snakecase) containing underscores to camelCase."""
    under_pat = re.compile(r'_([a-z])')
    return under_pat.sub(lambda x: x.group(1).upper(), name)


def param_list_to_dict(params: list) -> dict:
    """Converts AWS response objects to dicts.
    Many APIs return tags and other data objects in the following format:
    [{'Key': 'hello', 'Value': 'world'}, {'Key': 'hi', 'Value': 'there'}]

    This function converts the list of key-value pairs to a simple
    Python dictionary, making it much easier to parse.

    Example Output:
    {
        'hello': 'world',
        'hi': 'there'
    }
    """

    if params is None:
        return dict()
    else:
        return dict((el['Key'], el['Value']) for el in params)
