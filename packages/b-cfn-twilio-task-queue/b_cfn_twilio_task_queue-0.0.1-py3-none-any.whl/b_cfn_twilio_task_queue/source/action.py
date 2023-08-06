import json
import logging
import os
from typing import Dict, Any, Optional, Tuple

from twilio.base.exceptions import TwilioException
from twilio.rest import Client

logger = logging.getLogger(__name__)


class Action:
    def __init__(self, invocation_event: Dict[str, Any]):
        self.__invocation_event: Dict[str, Any] = invocation_event
        self.__parameters: Dict[str, Any] = invocation_event['ResourceProperties']
        self.__resource_id: Optional[str] = invocation_event.get('PhysicalResourceId')

        try:
            self.TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
            self.TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
            self.TWILIO_WORKSPACE_SID = os.environ['TWILIO_WORKSPACE_SID']
            self.TWILIO_TASK_QUEUE_NAME = self.__parameters['TwilioTaskQueueName']
        except KeyError as ex:
            logger.error(f'Missing environment: {repr(ex)}.')
            raise

        self.client = self.__get_twilio_client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

    def create(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Creates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource creation with these parameters: {json.dumps(self.__parameters)}.')

        task_queue = self.client.taskrouter.workspaces.get(self.TWILIO_WORKSPACE_SID).task_queues.create(self.TWILIO_TASK_QUEUE_NAME)
        task_queue_sid = task_queue.sid

        return {'TaskQueueSid': task_queue_sid}, task_queue_sid

    def update(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Updates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource update with these parameters: {json.dumps(self.__parameters)}.')

        task_queue_sid = self.__resource_id
        task_queue = self.client.taskrouter.workspaces.get(self.TWILIO_WORKSPACE_SID).task_queues.get(task_queue_sid).fetch()

        if task_queue.friendly_name != self.TWILIO_TASK_QUEUE_NAME:
            task_queue.update(friendly_name=self.TWILIO_TASK_QUEUE_NAME)

        return {'TaskQueueSid': task_queue_sid}, task_queue_sid

    def delete(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Deletes a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource deletion with these parameters: {json.dumps(self.__parameters)}.')

        task_queue_sid = self.__resource_id
        self.client.taskrouter.workspaces.get(self.TWILIO_WORKSPACE_SID).task_queues.get(task_queue_sid).delete()

        return {'TaskQueueSid': task_queue_sid}, task_queue_sid

    @staticmethod
    def __get_twilio_client(account_sid: str, auth_token: str) -> Client:
        """
        Creates a Twilio Client.

        :return: Twilio Client.
        """
        try:
            return Client(username=account_sid, password=auth_token)
        except TwilioException as ex:
            logger.error(f'Could not create Twilio client. Reason: {repr(ex)}.')
            raise
