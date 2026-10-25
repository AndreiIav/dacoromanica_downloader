import os
from io import BytesIO
from pathlib import Path
from urllib.request import url2pathname

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
        elif os.path.isdir(path):
            return 400, "Path Not A File"
        elif not os.path.isfile(path):
            return 404, "File Not Found"
        elif not os.access(path, os.R_OK):
            return 403, "Access Denied"
        else:
            return 200, "OK"

    def send(self, req, **kwargs):
        """Return the file specified by the given request

        @type req: C{PreparedRequest}
        """
        path = os.path.normcase(os.path.normpath(url2pathname(req.path_url)))
        response = requests.Response()

        response.status_code, response.reason = self._chkpath(req.method, path)

        if response.status_code == 200 and req.method.lower() != "head":
            try:
                response.raw = open(path, "rb")  # noqa
            except OSError as err:
                response.status_code = 500
                response.reason = str(err)

        # Ensure every response has a valid stream
        if response.raw is None:
            response.raw = BytesIO(b"")

        if isinstance(req.url, bytes):
            response.url = req.url.decode("utf-8")
        else:
            response.url = req.url

        response.request = req
        response.connection = self

        return response

    def close(self):
        pass


class TestHttpClient:
    def __init__(self, session: requests.Session):
        self.session = session
        self.timeout = (3.05, 27)
        self.chunk_size = 1024 * 1024

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def close(self) -> None:
        self.session.close()

    def patch_url(self, url: str) -> str:
        if "file:///" not in url:
            url_path = Path.cwd() / "tests" / "test_data" / "test_data_main" / url
            url = url_path.as_uri()
        return url

    def get_page(self, url: str) -> requests.Response:
        url = self.patch_url(url)
        response = self.session.get(url=url, timeout=self.timeout)
        response.raise_for_status()

        return response

    def download_file(self, url: str, file_path: Path) -> None:
        url = self.patch_url(url)
        with self.session.get(url, stream=True, timeout=self.timeout) as response:
            response.raise_for_status()

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=self.chunk_size):  # noqa: FURB122
                    file.write(chunk)


@pytest.fixture(scope="class")
def access_local_file_with_requests():
    requests_session = requests.Session()
    requests_session.mount("file:///", LocalFileAdapter())

    yield requests_session


@pytest.fixture
def get_path_to_test_file(test_file: str):
    test_file_path = Path("tests") / "test_data" / test_file
    test_file_path = test_file_path.resolve()
    file_link = test_file_path.as_uri()

    yield file_link


@pytest.fixture(scope="class")
def http_client(access_local_file_with_requests):
    http_client = TestHttpClient(session=access_local_file_with_requests)

    yield http_client
