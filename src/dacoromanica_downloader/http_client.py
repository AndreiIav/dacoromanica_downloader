from collections.abc import Collection
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HttpClient:
    def __init__(
        self,
        retry_total: int = 3,
        retry_backoff_factor: float = 0.1,
        retry_status_forcelist: Collection = (502, 503, 504),
        timeout: float | tuple = (3.05, 27),
        chunk_size: int = 1024 * 1024,  # 1 Mb
    ):
        self.session = requests.Session()
        self.retry_total = retry_total
        self.retry_backoff_factor = retry_backoff_factor
        self.retry_status_forcelist = retry_status_forcelist
        self.timeout = timeout
        self.chunk_size = chunk_size

        self._configure_retry(
            retry_total=self.retry_total,
            retry_backoff_factor=self.retry_backoff_factor,
            retry_status_forcelist=self.retry_status_forcelist,
        )
        self._update_headers()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def close(self) -> None:
        self.session.close()

    def _update_headers(self):
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0",
            }
        )

    def _configure_retry(
        self,
        retry_total: int,
        retry_backoff_factor: float,
        retry_status_forcelist: Collection,
    ) -> None:
        retries = Retry(
            total=retry_total,
            backoff_factor=retry_backoff_factor,
            status_forcelist=retry_status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retries)

        self.session.mount(prefix="http://", adapter=adapter)
        self.session.mount(prefix="https://", adapter=adapter)

    def get_page(self, url: str) -> requests.Response:
        response = self.session.get(url=url, timeout=self.timeout)
        response.raise_for_status()

        return response

    def download_file(self, url: str, file_path: Path) -> None:
        with self.session.get(url, stream=True, timeout=self.timeout) as response:
            response.raise_for_status()

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=self.chunk_size):  # noqa: FURB122
                    file.write(chunk)
