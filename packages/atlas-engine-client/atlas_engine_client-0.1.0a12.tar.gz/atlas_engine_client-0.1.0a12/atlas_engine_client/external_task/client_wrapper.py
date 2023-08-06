from atlas_engine_client import external_task
from .external_task_client import ExternalTaskClient


class ClientWrapper:

    def __init__(self, atlas_engine_url):
        self._atlas_engine_url = atlas_engine_url

    def subscribe_to_external_task_for_topic(self, topic, handler):
        external_task_client = ExternalTaskClient(self._atlas_engine_url)

        external_task_client.subscribe_to_external_task_for_topic(topic, handler)

        return external_task_client
        
