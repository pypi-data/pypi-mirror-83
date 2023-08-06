from dbks.client import Client


class LibraryAPI:
    def __init__(self, client=Client()):
        self.client = client

    def all_cluster_statuses(self, params=None, json=None):
        return self.client.call("GET", "/libraries/all-cluster-statuses")

    def cluster_status(self, params=None, json=None):
        return self.client.call("GET", "/libraries/cluster-status", params=params)

    def install(self, params=None, json=None):
        return self.client.call("POST", "/libraries/install", json=json)

    def uninstall(self, params=None, json=None):
        return self.client.call("POST", "/libraries/uninstall", json=json)
