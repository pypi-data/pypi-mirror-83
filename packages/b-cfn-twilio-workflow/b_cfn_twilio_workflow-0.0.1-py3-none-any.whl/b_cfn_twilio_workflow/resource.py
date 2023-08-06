from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio_workflow.function import TwilioWorkflowSingletonFunction


class TwilioWorkflowResource(CustomResource):
    """
    Custom resource used for managing a Twilio workflow for a deployment.

    Creates a workflow on stack creation.
    Updates the workflow on workflow name change.
    Deletes the workflow on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            workflow_function: TwilioWorkflowSingletonFunction,
            workflow_name: str
    ) -> None:
        super().__init__(
            scope=scope,
            id=f'CustomResource{workflow_function.function_name}',
            service_token=workflow_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'TwilioWorkflowName': workflow_name
            }
        )

    @property
    def workflow_sid(self):
        return self.get_att_string("WorkflowSid")
