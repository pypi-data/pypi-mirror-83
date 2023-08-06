from dbks.client import Client


class WorkspaceAPI:
    def __init__(self, client=Client()):
        self.client = client

    def delete(self, params=None, json=None):
        return self.client.call("POST", "/workspace/delete", json=json)

    def export(self, params=None, json=None):
        return self.client.call("GET", "/workspace/export", json=json)

    def get_status(self, params=None, json=None):
        return self.client.call("GET", "/workspace/get-status", json=json)

    def _import(self, params=None, json=None):
        return self.client.call("POST", "/workspace/import", json=json)

    def list(self, params=None, json=None):
        return self.client.call("GET", "/workspace/list", json=json)

    def mkdirs(self, params=None, json=None):
        return self.client.call("POST", "/workspace/mkdirs", json=json)
