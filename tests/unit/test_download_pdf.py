import pytest
import requests

from dacoromanica_downloader.download_pdf import (
    PathTooLongError,
    download_file,
    get_link_response,
    shorten_filename,
)


class TestShortenFilename:
    def test_shorten_filename_shortens_filename_that_is_over_limit(self):
        limit = 250
        extension = ".pdf"  # 4 characters
        path = ("h" * 5) + "/"  # 6 characters
        file_name_within_limit = "a" * 240
        file_name_over_limit = "b" * 5
        filename = f"{path}{file_name_within_limit}{file_name_over_limit}{extension}"

        formated_filename = shorten_filename(filename)

        assert len(str(formated_filename)) == limit
        assert str(formated_filename) == f"{path}{file_name_within_limit}{extension}"

    def test_shorten_filename_does_not_shorten_name_that_is_not_over_limit(self):
        limit = 250
        extension = ".pdf"  # 4 characters
        path = ("h" * 5) + "/"  # 6 characters
        file_name_within_limit = "a" * 240
        filename = f"{path}{file_name_within_limit}{extension}"

        formated_filename = shorten_filename(filename)

        assert len(str(formated_filename)) == limit
        assert str(formated_filename) == f"{path}{file_name_within_limit}{extension}"

    def test_shorten_filename_raises_exception_if_filename_can_not_be_shortened(self):
        extension = ".pdf"  # 4 characters
        path = ("h" * 249) + "/"  # 250 charactes
        file_name = "a" * 10
        filename = f"{path}{file_name}{extension}"

        with pytest.raises(PathTooLongError) as e:
            shorten_filename(filename)

        assert (
            f"'{filename}' file name is too long and cannot be saved."
            " File not downloaded." in str(e.value)
        )


class TestGetLinkResponse:
    @pytest.mark.parametrize("test_file", ["test_page.html"])
    def test_get_link_response_returns_response_object_when_successful(
        self, access_local_file_with_requests, get_path_to_test_file
    ):
        file_link = get_path_to_test_file

        response = get_link_response(file_link, access_local_file_with_requests)

        assert isinstance(response, requests.Response)
        assert response.status_code == 200


class TestDownloadFile:
    @pytest.mark.parametrize("test_file", ["test.pdf"])
    def test_download_file_downloads_file(
        self, tmp_path, access_local_file_with_requests, get_path_to_test_file
    ):
        filename = tmp_path / "downloaded_test_file.pdf"
        file_link = get_path_to_test_file
        http_response = get_link_response(file_link, access_local_file_with_requests)

        download_file(filename=filename, http_response=http_response)

        assert filename.is_file()
