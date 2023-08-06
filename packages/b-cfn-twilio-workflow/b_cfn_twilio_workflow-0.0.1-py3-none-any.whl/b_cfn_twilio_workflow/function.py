from __future__ import annotations

from functools import lru_cache

from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack

from b_twilio_sdk_layer.layer import Layer as TwilioLayer


class TwilioWorkflowSingletonFunction(SingletonFunction):
    """
    Custom workflow resource Singleton Lambda function.

    Creates a workflow on stack creation.
    Updates the workflow on workflow name change.
    Deletes the workflow on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            name: str,
            twilio_account_sid: str,
            twilio_auth_token: str,
            twilio_workspace_sid: str,
            twilio_task_queue_sid: str
    ) -> None:
        self.__name = name

        super().__init__(
            scope=scope,
            id=name,
            uuid=f'{name}-uuid',
            function_name=name,
            code=self.__code(),
            layers=[TwilioLayer(scope, f'TwilioLayerFor{name}')],
            handler='index.handler',
            runtime=Runtime.PYTHON_3_8,
            environment={
                'TWILIO_ACCOUNT_SID': twilio_account_sid,
                'TWILIO_AUTH_TOKEN': twilio_auth_token,
                'TWILIO_WORKSPACE_SID': twilio_workspace_sid,
                'TWILIO_TASK_QUEUE_SID': twilio_task_queue_sid
            }
        )

    @lru_cache
    def __code(self) -> Code:
        from .source import root
        return Code.from_asset(root)

    @property
    def function_name(self):
        return self.__name
