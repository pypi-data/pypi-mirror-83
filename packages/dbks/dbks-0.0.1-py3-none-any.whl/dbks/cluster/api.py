from dbks.client import Client


class ClusterAPI:
    def __init__(self, client=Client()):
        self.client = client

    def create(self, params=None, json=None):
        return self.client.call("POST", "/clusters/create", json=json)

    def edit(self, params=None, json=None):
        return self.client.call("POST", "/clusters/edit", json=json)

    def start(self, params=None, json=None):
        return self.client.call("POST", "/clusters/start", json=json)

    def restart(self, params=None, json=None):
        return self.client.call("POST", "/clusters/restart", json=json)

    def resize(self, params=None, json=None):
        return self.client.call("POST", "/clusters/resize", json=json)

    def terminate(self, params=None, json=None):
        return self.client.call("POST", "/clusters/delete", json=json)

    def delete(self, params=None, json=None):
        return self.client.call("POST", "/clusters/permanent-delete", json=json)

    def get(self, params=None, json=None):
        return self.client.call("GET", "/clusters/get", params=params)

    def pin(self, params=None, json=None):
        return self.client.call("POST", "/clusters/pin", json=json)

    def unpin(self, params=None, json=None):
        return self.client.call("POST", "/clusters/unpin", json=json)

    def list(self, params=None, json=None):
        return self.client.call("GET", "/clusters/list")

    def list_node_types(self, params=None, json=None):
        return self.client.call("GET", "/clusters/list-node-types")

    def runtime_versions(self, params=None, json=None):
        return self.client.call("GET", "/clusters/spark-versions")

    def list_zones(self, params=None, json=None):
        return self.client.call("GET", "/clusters/list-zones")

    def events(self, params=None, json=None):
        return self.client.call("POST", "/clusters/events", json=json)
