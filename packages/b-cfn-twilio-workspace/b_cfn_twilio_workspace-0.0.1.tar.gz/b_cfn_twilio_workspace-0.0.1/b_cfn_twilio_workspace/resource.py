from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio_workspace.function import TwilioWorkspaceSingletonFunction


class TwilioWorkspaceResource(CustomResource):
    """
    Custom resource used for managing a Twilio workspace for a deployment.

    Creates a workspace on stack creation.
    Updates the workspace on workspace name change.
    Deletes the workspace on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            workspace_function: TwilioWorkspaceSingletonFunction,
            workspace_name: str
    ) -> None:
        super().__init__(
            scope=scope,
            id=f'CustomResource{workspace_function.function_name}',
            service_token=workspace_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'TwilioWorkspaceName': workspace_name
            }
        )

    @property
    def workspace_sid(self):
        return self.get_att_string("WorkspaceSid")
