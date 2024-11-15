from functools import partial
from pathlib import Path

import pytest
import requests

from dacoromanica_downloader.main import main


def new_get_link_response(
    link: str, get_request: requests.get
) -> requests.Response | str:
    """
    Version of get_link_response() that works with local html files.
    Needed for making accessing local html files from relative paths work.
    """
    if "file:///" not in link:
        link_path = (
            Path(".").resolve() / "tests" / "test_data" / "test_data_main" / link
        )
        link = "file:///" + str(link_path)
    try:
        response = get_request(link, timeout=20)
        return response
    except requests.exceptions.HTTPError as e:
        return f"HTTPError : {e}"
    except requests.exceptions.ConnectionError as e:
        return f"ConnectionError : {e}"
    except requests.exceptions.Timeout as e:
        return f"Timeout exception : {e}"
    except requests.exceptions.RequestException as e:
        return f"RequestException : {e}"


class TestMain:
    @pytest.mark.parametrize("test_file", ["test_data_main/collections_page1.html"])
    def test_main_end_to_end_happy_path(
        self,
        monkeypatch,
        get_path_to_test_file,
        access_local_file_with_requests,
        tmp_path,
        capsys,
    ):
        link = get_path_to_test_file
        test_get_link_response = partial(
            new_get_link_response,
            link=link,
            get_request=access_local_file_with_requests,
        )

        monkeypatch.setattr(
            "dacoromanica_downloader.main.get_link_response",
            test_get_link_response,
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.starting_urls",
            [link],
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.next_page_link_identifier",
            "table_view_collections",
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.collections_base_link_identifier",
            "collection_details",
        )
        destination_location = tmp_path
        monkeypatch.setattr(
            "dacoromanica_downloader.main.destination_folder", destination_location
        )
        files_to_be_downloaded_location = (
            Path(".").resolve() / "tests" / "test_data" / "test_data_main"
        )
        files_to_be_downloaded = [
            "collection1.pdf",
            "collection2.pdf",
            "collection3.pdf",
            "collection4.pdf",
        ]
        expected_downloaded_files = [
            "Author 1_Title 1_1900.pdf",
            "Author 2_Title 2_1903.pdf",
            "Author 3_Title 3.pdf",
            "Title 4_1850.pdf",
        ]

        main()

        out, _ = capsys.readouterr()
        for file in zip(files_to_be_downloaded, expected_downloaded_files):
            file_to_be_downloaded = files_to_be_downloaded_location / file[0]
            downloaded_file = Path(destination_location) / file[1]
            downloaded_file_name = file[1]

            assert (
                f"'{downloaded_file_name}' downloaded in '{destination_location}' folder."
                in out
            )
            assert downloaded_file.is_file()
            assert Path.read_bytes(file_to_be_downloaded) == Path.read_bytes(
                downloaded_file
            )

        assert "dacoromanica_downloader finished." in out

    def test_main_starting_link_cannot_be_accessed(
        self,
        monkeypatch,
        capsys,
    ):
        link = "link/"
        monkeypatch.setattr(
            "dacoromanica_downloader.main.starting_urls",
            [link],
        )

        main()

        out, _ = capsys.readouterr()
        assert f"{link} could not be accessed" in out

    def test_main_starting_link_contains_no_table_view_link(self, monkeypatch, capsys):
        link = "https://link.com"
        monkeypatch.setattr(
            "dacoromanica_downloader.main.starting_urls",
            [link],
        )

        main()

        out, _ = capsys.readouterr()
        assert f"'{link}' is not a valid Dacoromanica collections page. " in out

    @pytest.mark.parametrize("test_file", ["test_data_main/collections_page2.html"])
    def test_main_table_link_view_cannot_be_accessed(
        self,
        monkeypatch,
        get_path_to_test_file,
        access_local_file_with_requests,
        capsys,
    ):
        link = get_path_to_test_file
        test_get_link_response = partial(
            new_get_link_response,
            link=link,
            get_request=access_local_file_with_requests,
        )

        monkeypatch.setattr(
            "dacoromanica_downloader.main.get_link_response",
            test_get_link_response,
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.starting_urls",
            [link],
        )

        main()

        out, _ = capsys.readouterr()
        assert "The table view cannot be accessed" in out

    @pytest.mark.parametrize("test_file", ["test_data_main/collections_page3.html"])
    def test_main_next_page_cannot_be_accessed(
        self,
        monkeypatch,
        get_path_to_test_file,
        access_local_file_with_requests,
        capsys,
    ):
        link = get_path_to_test_file
        test_get_link_response = partial(
            new_get_link_response,
            link=link,
            get_request=access_local_file_with_requests,
        )

        monkeypatch.setattr(
            "dacoromanica_downloader.main.get_link_response",
            test_get_link_response,
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.starting_urls",
            [link],
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.next_page_link_identifier",
            "table_view_collections",
        )

        main()

        out, _ = capsys.readouterr()
        assert "'not_existent_table_view_collections' could not be accessed" in out

    @pytest.mark.parametrize("test_file", ["test_data_main/collections_page3.html"])
    def test_main_collection_details_page_cannot_be_accessed(
        self,
        monkeypatch,
        get_path_to_test_file,
        access_local_file_with_requests,
        capsys,
        tmp_path,
    ):
        link = get_path_to_test_file
        test_get_link_response = partial(
            new_get_link_response,
            link=link,
            get_request=access_local_file_with_requests,
        )

        monkeypatch.setattr(
            "dacoromanica_downloader.main.get_link_response",
            test_get_link_response,
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.starting_urls",
            [link],
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.next_page_link_identifier",
            "table_view_collections",
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.collections_base_link_identifier",
            "collection_details",
        )
        destination_location = tmp_path
        monkeypatch.setattr(
            "dacoromanica_downloader.main.destination_folder", destination_location
        )
        file_to_be_downloaded_location = (
            Path(".").resolve() / "tests" / "test_data" / "test_data_main"
        )
        file_to_be_downloaded = [
            "collection1.pdf",
        ]

        # the collection_detail page won't be accessed so the year will be
        # missing from the filename
        expected_downloaded_file = [
            "Author 1_Title 1.pdf",
        ]

        main()

        out, _ = capsys.readouterr()
        for file in zip(file_to_be_downloaded, expected_downloaded_file):
            file_to_be_downloaded = file_to_be_downloaded_location / file[0]
            downloaded_file = Path(destination_location) / file[1]
            downloaded_file_name = file[1]

            assert (
                f"'{downloaded_file_name}' downloaded in '{destination_location}' folder."
                in out
            )
            assert downloaded_file.is_file()

    @pytest.mark.parametrize("test_file", ["test_data_main/collections_page4.html"])
    def test_main_collection_pdf_page_cannot_be_accessed(
        self,
        monkeypatch,
        get_path_to_test_file,
        access_local_file_with_requests,
        capsys,
    ):
        link = get_path_to_test_file
        test_get_link_response = partial(
            new_get_link_response,
            link=link,
            get_request=access_local_file_with_requests,
        )

        monkeypatch.setattr(
            "dacoromanica_downloader.main.get_link_response",
            test_get_link_response,
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.starting_urls",
            [link],
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.next_page_link_identifier",
            "table_view_collections",
        )
        monkeypatch.setattr(
            "dacoromanica_downloader.main.collections_base_link_identifier",
            "collection_details",
        )

        main()

        out, _ = capsys.readouterr()
        assert "'Title 1' was not downloaded" in out
