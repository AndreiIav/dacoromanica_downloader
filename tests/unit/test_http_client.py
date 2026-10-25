from unittest.mock import MagicMock, patch

from dacoromanica_downloader.http_client import HttpClient


class TestHttpClient:
    def test_get_page(self):
        url = "https://example.com"
        status_code = 200

        mock_response = MagicMock()
        mock_response.status_code = status_code

        with (
            HttpClient() as http_client,
            patch.object(
                http_client.session, "get", return_value=mock_response
            ) as mock_get,
        ):
            response = http_client.get_page(url)

            assert response.status_code == status_code
            mock_get.assert_called_once_with(url=url, timeout=http_client.timeout)

    def test_download_file(self, tmp_path):
        url = "https://example.com/file.txt"
        file_path = tmp_path / "file.txt"
        file_content = b"Data Content"

        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.iter_content.return_value = [file_content]

        with (
            HttpClient() as http_client,
            patch.object(
                http_client.session, "get", return_value=mock_response
            ) as mock_get,
        ):
            http_client.download_file(url=url, file_path=file_path)

            assert file_path.read_bytes() == file_content
            mock_get.assert_called_once_with(
                url, stream=True, timeout=http_client.timeout
            )
