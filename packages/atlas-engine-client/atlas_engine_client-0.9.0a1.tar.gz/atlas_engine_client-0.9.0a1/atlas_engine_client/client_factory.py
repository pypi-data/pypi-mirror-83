from atlas_engine_client.external_task import ClientWrapper


class ClientFactory:

    def __init__(self):
        pass

    def create_external_task_client(self, atlas_engine_url):
        return ClientWrapper(atlas_engine_url)