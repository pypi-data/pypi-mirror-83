
from typing import Literal

from pydantic import BaseModel


class ARN(BaseModel):
    arn: str
    partition: Literal['aws', 'aws-cn', 'aws-us-gov']
    service: str
    region: str
    accountId: str
    resourceType: str or None = None
    resourceId: str
