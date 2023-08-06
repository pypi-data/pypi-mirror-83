from dbks.client import Client


class PermissionAPI:
    def __init__(self, client=Client()):
        self.client = client

    # cluster permissions
    def get_cluster_permission_levels(self, params=None, json=None):
        return self.client.call(
            "GET", f"/permissions/clusters/{params['cluster_id']}/permissionLevels"
        )

    def get_cluster_permissions(self, params=None, json=None):
        return self.client.call("GET", f"/permissions/clusters/{params['cluster_id']}")

    def update_cluster_permissions(self, params=None, json=None):
        return self.client.call(
            "PATCH", f"/permissions/clusters/{params['cluster_id']}", json=json
        )

    def replace_cluster_permissions(self, params=None, json=None):
        return self.client.call(
            "PUT", f"/permissions/clusters/{params['cluster_id']}", json=json
        )

    # directory permissions
    def get_directory_permission_levels(self, params=None, json=None):
        return self.client.call(
            "GET", f"/permissions/directories/{params['directory_id']}/permissionLevels"
        )

    def get_directory_permissions(self, params=None, json=None):
        return self.client.call(
            "GET", f"/permissions/directories/{params['directory_id']}"
        )

    def update_directory_permissions(self, params=None, json=None):
        return self.client.call(
            "PATCH", f"/permissions/directories/{params['directory_id']}", json=json
        )

    def replace_directory_permissions(self, params=None, json=None):
        return self.client.call(
            "PUT", f"/permissions/directories/{params['directory_id']}", json=json
        )
