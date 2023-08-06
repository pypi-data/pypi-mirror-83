from dbks.cluster.api import ClusterAPI
from dbks.response_handler import ResponseHandler
from dbks.util import same_as_target


class ClusterController:
    def __init__(self, api=ClusterAPI()):
        if not isinstance(api, ClusterAPI):
            raise ValueError("Parameter must be an instance of ClusterAPI!")
        self.api = api

    @ResponseHandler
    def list(self):
        return self.api.list()

    @ResponseHandler
    def get(self, cluster_id):
        return self.api.get(params={"cluster_id": cluster_id})

    @ResponseHandler
    def create(self, cluster_def):
        return self.api.create(json=cluster_def)

    @ResponseHandler
    def edit(self, cluster_id, cluster_def):
        cluster_def["cluster_id"] = cluster_id
        return self.api.edit(json=cluster_def)

    @ResponseHandler
    def start(self, cluster_id):
        return self.api.start(json={"cluster_id": cluster_id})

    @ResponseHandler
    def pin(self, cluster_id):
        return self.api.pin(json={"cluster_id": cluster_id})

    @ResponseHandler
    def unpin(self, cluster_id):
        return self.api.unpin(json={"cluster_id": cluster_id})

    @ResponseHandler
    def delete(self, cluster_id):
        return self.api.delete(json={"cluster_id": cluster_id})

    def get_id_by_name(self, cluster_name=""):
        cluster_ids = []
        if not cluster_name:
            raise ValueError("Please provide cluster name string!")
        res = self.list()
        clusters = res.json()["clusters"]
        for cluster in clusters:
            if cluster["cluster_name"] == cluster_name:
                cluster_ids.append(cluster["cluster_id"])
        return cluster_ids

    def create_or_edit_cluster(self, cluster_def, pin=True):
        cluster_name = cluster_def["cluster_name"]
        cluster_id = None
        cluster_ids = self.get_id_by_name(cluster_name)
        resp = None
        if not cluster_ids:
            print(f'cluster "{cluster_name}" does not exist, creating...')
            resp = self.create(cluster_def)
            cluster_id = resp.json()["cluster_id"]
            if pin:
                self.pin(cluster_id)
        elif len(cluster_ids) == 1:
            print(f'cluster "{cluster_name}" already exists, compare spec...')
            cluster_id = cluster_ids[0]
            current_def = self.get(cluster_id).json()
            if not same_as_target(cluster_def, current_def):
                (f'cluster "{cluster_name}" spec changed, editing...')
                resp = self.edit(cluster_id, cluster_def)
            else:
                print("specs are the same, skipping ...")
            if pin:
                self.pin(cluster_id)
            else:
                self.unpin(cluster_id)
        else:
            raise Exception(
                f'Found multiple clusters {cluster_ids} with name [{cluster_def["cluster_name"]}]!'
            )
        return resp

    def delete_by_name(self, cluster_name=""):
        cluster_ids = self.get_id_by_name(cluster_name)
        if not cluster_ids:
            print(f'cluster "{cluster_name}" does not exist, aborting...')
            return None
        elif len(cluster_ids) == 1:
            print(f'cluster "{cluster_name}" found, deleting...')
            cluster_id = cluster_ids[0]
            self.unpin(cluster_id)
            return self.delete(cluster_id)
        else:
            raise Exception(
                f'Found multiple clusters {cluster_ids} with name "{cluster_name}"!'
            )
