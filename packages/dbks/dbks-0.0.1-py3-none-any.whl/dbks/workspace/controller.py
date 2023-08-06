import base64
from pathlib import Path
from dbks.workspace.api import WorkspaceAPI
from dbks.response_handler import ResponseHandler


class WorkspaceController:
    def __init__(self, api=WorkspaceAPI()):
        if not isinstance(api, WorkspaceAPI):
            raise ValueError("Parameter must be an instance of WorkspaceAPI!")
        self.api = api

    @ResponseHandler
    def delete(self, path, recursive=True):
        return self.api.delete(json={"path": path, "recursive": recursive})

    @ResponseHandler
    def export(self, path, format="SOURCE"):
        return self.api.export(json={"path": path, "format": format})

    @ResponseHandler
    def get_status(self, path):
        return self.api.get_status(json={"path": path})

    @ResponseHandler
    def _import(self, local_path, path, language, overwrite=False, format="SOURCE"):
        # This has a limit of 10 MB
        content = ""
        with open(local_path, "r") as file:
            content = file.read()
        return self.api._import(
            json={
                "content": base64.b64encode(bytes(content, "utf-8")).decode(),
                "path": path,
                "language": language.upper(),
                "overwrite": overwrite,
                "format": format,
            }
        )

    @ResponseHandler
    def list(self, path):
        return self.api.list(json={"path": path})

    @ResponseHandler
    def mkdirs(self, path):
        return self.api.mkdirs(json={"path": path})

    # create folder is not exists
    def imports(self, local_path, path, language, overwrite=False, format="SOURCE"):
        target_path = Path(path)
        self.mkdirs(str(target_path.parent))
        self._import(
            local_path=local_path,
            path=path,
            language=language,
            overwrite=overwrite,
            format=format,
        )

    def get_id_by_path(self, path):
        return self.get_status(path).json()["object_id"]
