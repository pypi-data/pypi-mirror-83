from dbks.permission.api import PermissionAPI
from dbks.response_handler import ResponseHandler


class PermissionController:
    def __init__(self, api=PermissionAPI()):
        if not isinstance(api, PermissionAPI):
            raise ValueError("Parameter must be an instance of PermissionAPI!")
        self.api = api

    @ResponseHandler
    def get_cluster_permission_levels(self, cluster_id):
        return self.api.get_cluster_permission_levels(params={"cluster_id": cluster_id})

    @ResponseHandler
    def get_cluster_permissions(self, cluster_id):
        return self.api.get_cluster_permissions(params={"cluster_id": cluster_id})

    @ResponseHandler
    def update_cluster_permissions(self, cluster_id, access_control_list):
        """
        This request only grants (adds) permissions.
        To revoke, use "replace_cluster_permissions".

        "access_control_list" example input:
            [
                {
                    "user_name": "jsmith@example.com",
                    "permission_level": "CAN_RESTART"
                },
                ...
            ]
        """
        return self.api.update_cluster_permissions(
            params={"cluster_id": cluster_id},
            json={"access_control_list": access_control_list},
        )

    @ResponseHandler
    def replace_cluster_permissions(self, cluster_id, access_control_list):
        """
        WARNING: This request overwrites all existing direct (non-inherited)
        permissions on the cluster and replaces it with the new permissions
        specified in the request body.

        "access_control_list" example input:
            [
                {
                    "user_name": "jsmith@example.com",
                    "permission_level": "CAN_RESTART"
                },
                ...
            ]
        """
        return self.api.replace_cluster_permissions(
            params={"cluster_id": cluster_id},
            json={"access_control_list": access_control_list},
        )

    @ResponseHandler
    def get_directory_permission_levels(self, directory_id):
        return self.api.get_directory_permission_levels(
            params={"directory_id": directory_id}
        )

    @ResponseHandler
    def get_directory_permissions(self, directory_id):
        return self.api.get_directory_permissions(params={"directory_id": directory_id})

    @ResponseHandler
    def update_directory_permissions(self, directory_id, access_control_list):
        """
        This request only grants (adds) permissions.
        To revoke, use "replace_directory_permissions".

        "access_control_list" example input:
            [
                {
                    "user_name": "jsmith@example.com",
                    "permission_level": "CAN_READ"
                },
                ...
            ]
        """
        return self.api.update_directory_permissions(
            params={"directory_id": directory_id},
            json={"access_control_list": access_control_list},
        )

    @ResponseHandler
    def replace_directory_permissions(self, directory_id, access_control_list):
        """
        WARNING: This request overwrites all existing direct (non-inherited)
        permissions on the directory and replaces it with the new permissions
        specified in the request body.

        "access_control_list" example input:
            [
                {
                    "user_name": "jsmith@example.com",
                    "permission_level": "CAN_RUN"
                },
                ...
            ]
        """
        return self.api.replace_directory_permissions(
            params={"directory_id": directory_id},
            json={"access_control_list": access_control_list},
        )
