from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio_task_queue.function import TwilioTaskQueueSingletonFunction


class TwilioTaskQueueResource(CustomResource):
    """
    Custom resource used for managing a Twilio task_queue for a deployment.

    Creates a task_queue on stack creation.
    Updates the task_queue on task_queue name change.
    Deletes the task_queue on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            task_queue_function: TwilioTaskQueueSingletonFunction,
            task_queue_name: str
    ) -> None:
        super().__init__(
            scope=scope,
            id=f'CustomResource{task_queue_function.function_name}',
            service_token=task_queue_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'TwilioTaskQueueName': task_queue_name,
            }
        )

    @property
    def task_queue_sid(self):
        return self.get_att_string('TaskQueueSid')
