"""Conversion.

Utility functions that assist with common (or helpful) conversions.
"""
import logging

from .data_classes.arn import ARN, arn

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
