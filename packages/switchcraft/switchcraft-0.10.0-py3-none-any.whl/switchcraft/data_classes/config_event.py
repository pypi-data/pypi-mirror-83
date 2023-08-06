"""Config Event.

Data Classes representing AWS Config Events.
"""

from switchcraft.data_classes.base import DictWrapper


class ConfigInvokingEvent(DictWrapper):
    @property
    def account_id(self) -> str:
        """Returns the account id of the account where the event originated."""
        return self['awsAccountId']

    @property
    def notification_creation_time(self) -> str:
        """Returns a timestamp representing the creation date/time."""
        return self['notificationCreationTime']

    @property
    def message_type(self) -> str:
        """Returns the type of the AWS Config message."""
        return self['messageType']


class ConfigEvent(DictWrapper):
    """An AWS Config Scheduled Event."""

    @property
    def invoking_event(self) -> ConfigInvokingEvent:
        return ConfigInvokingEvent(self['invokingEvent'])

    @property
    def result_token(self) -> str:
        """Returns a result token.

        Result tokens ensure that results for the originating event can
        easily be returned to the AWS Config service.
        """
        return self['resultToken']

    @property
    def event_left_scope(self) -> bool:
        return self['eventLeftScope']

    @property
    def execution_role_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the role used to execute the
        rule."""
        return self['executionRoleArn']

    @property
    def config_rule_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the AWS Config Rule."""
        return self['configRuleArn']

    @property
    def config_rule_name(self) -> str:
        """Returns the name of the AWS Config Rule."""
        return self['configRuleName']

    @property
    def config_rule_id(self) -> str:
        """Returns the ID of the AWS Config Rule."""
        return self['configRuleId']

    @property
    def account_id(self) -> str:
        """Returns the AWS Account ID."""
        return self['accountId']
