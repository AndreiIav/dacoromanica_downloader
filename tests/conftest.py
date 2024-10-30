from pathlib import Path

import pytest
import requests


# from this SO answer:
# https://stackoverflow.com/a/27786580
class LocalFileAdapter(requests.adapters.BaseAdapter):
    """Protocol Adapter to allow Requests to GET file:// URLs"""

    @staticmethod
    def _chkpath(method, path):
        """Return an HTTP status for the given filesystem path."""
        if method.lower() in ("put", "delete"):
            return 501, "Not Implemented"
        elif method.lower() not in ("get", "head"):
            return 405, "Method Not Allowed"
        elif Path.is_dir(path):
            return 400, "Path Not A File"
        elif not Path.is_file(path):
            return 404, "File Not Found"
        else:
            return 200, "OK"

    def send(self, req, **kwargs):
        """Return the file specified by the given request

        @type req: C{PreparedRequest}
        """
        path = Path(req.path_url)
        response = requests.Response()

        response.status_code, response.reason = self._chkpath(req.method, path)
        if response.status_code == 200 and req.method.lower() != "head":
            try:
                response.raw = open(path, "rb")
            except (OSError, IOError) as err:
                response.status_code = 500
                response.reason = str(err)

        if isinstance(req.url, bytes):
            response.url = req.url.decode("utf-8")
        else:
            response.url = req.url

        response.request = req
        response.connection = self

        return response

    def close(self):
        pass


@pytest.fixture
def access_local_file_with_requests():
    requests_session = requests.Session()
    requests_session.mount("file://", LocalFileAdapter())

    yield requests_session.get


@pytest.fixture
def get_path_to_test_file(test_file: str):
    test_file_path = Path("tests") / "test_data" / test_file
    test_file_path = test_file_path.absolute()
    file_link = f"file://{str(test_file_path)}"

    yield file_link
