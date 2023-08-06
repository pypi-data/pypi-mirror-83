from atlas_engine_client.app_info import AppInfoClient
from atlas_engine_client.external_task import ClientWrapper
from atlas_engine_client.flow_node_instance import FlowNodeInstanceClient
from atlas_engine_client.notification import NotifcationClient
from atlas_engine_client.process_instance import ProcessInstanceClient
from atlas_engine_client.process_model import ProcessModelClient
from atlas_engine_client.user_task import UserTaskClient


class ClientFactory:

    def __init__(self):
        pass

    def create_app_info_client(self, engine_url):
        return AppInfoClient(engine_url)

    def create_external_task_client(self, engine_url):
        return ClientWrapper(engine_url)

    def create_flow_node_instance_client(self, engine_url):
        return FlowNodeInstanceClient(engine_url)

    def create_notification_client(self, engine_url):
        return NotifcationClient(engine_url)

    def create_process_instance_client(self, engine_url):
        return ProcessInstanceClient(engine_url)

    def create_process_model_client(self, engine_url):
        return ProcessModelClient(engine_url)

    def create_user_task_client(self, engine_url):
        return UserTaskClient(engine_url)

    