from functools import partial
from pathlib import Path

import pytest
import requests

from dacoromanica_downloader.application import run_dacoromanica_downloader


def new_get_link_response(
    link: str, get_request: requests.get
) -> requests.Response | str:
    """
    Version of get_link_response() that works with local html files.
    Needed for making accessing local html files from relative paths work.
    """
    if "file:///" not in link:
        link_path = Path.cwd() / "tests" / "test_data" / "test_data_main" / link
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


def do_not_wait(_seconds: float) -> None:
    pass


class TestRunApplication:
    @pytest.mark.parametrize("test_file", ["test_data_main/collections_page1.html"])
    def test_run_application_end_to_end_happy_path(
        self,
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

        starting_urls = [link]
        next_page_link_identifier = "table_view_collections"
        collections_base_link_identifier = "collection_details"
        destination_location = tmp_path

        files_to_be_downloaded_location = (
            Path.cwd() / "tests" / "test_data" / "test_data_main"
        )
        files_to_be_downloaded = [
            "collection1.pdf",
            "collection2.pdf",
            "collection3.pdf",
            "collection4.pdf",
            "collection5.pdf",
            "collection6.pdf",
        ]
        expected_downloaded_files = [
            "Author 1_Title 1_1900.pdf",
            "Author 2_Title 2_1903.pdf",
            "Author 3_Title 3.pdf",
            "Title 4_1850.pdf",
            "Author 5_Title 5_1600.pdf",
            "Author 6_Title 6_1700.pdf",
        ]

        run_dacoromanica_downloader(
            starting_urls=starting_urls,
            destination_folder=destination_location,
            next_page_link_identifier=next_page_link_identifier,
            collections_base_link_identifier=collections_base_link_identifier,
            get_response=test_get_link_response,
            wait=do_not_wait,
        )

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

    def test_run_application_starting_link_cannot_be_accessed(self, capsys, tmp_path):
        link = "link/"
        starting_urls = [link]
        next_page_link_identifier = "table_view_collections"
        collections_base_link_identifier = "collection_details"
        destination_location = tmp_path

        run_dacoromanica_downloader(
            starting_urls=starting_urls,
            destination_folder=destination_location,
            next_page_link_identifier=next_page_link_identifier,
            collections_base_link_identifier=collections_base_link_identifier,
        )

        out, _ = capsys.readouterr()
        assert f"{link} could not be accessed" in out

    @pytest.mark.parametrize(
        "test_file", ["test_data_main/collections_page_no_table_view.html"]
    )
    def test_run_application_starting_link_contains_no_table_view_link(
        self, get_path_to_test_file, access_local_file_with_requests, tmp_path, capsys
    ):
        link = get_path_to_test_file
        test_get_link_response = partial(
            new_get_link_response,
            link=link,
            get_request=access_local_file_with_requests,
        )
        starting_urls = [link]
        next_page_link_identifier = "table_view_collections"
        collections_base_link_identifier = "collection_details"
        destination_location = tmp_path

        run_dacoromanica_downloader(
            starting_urls=starting_urls,
            destination_folder=destination_location,
            next_page_link_identifier=next_page_link_identifier,
            collections_base_link_identifier=collections_base_link_identifier,
            get_response=test_get_link_response,
            wait=do_not_wait,
        )

        out, _ = capsys.readouterr()
        assert f"'{link}' is not a valid Dacoromanica collections page. " in out

    @pytest.mark.parametrize("test_file", ["test_data_main/collections_page3.html"])
    def test_run_application_collection_details_page_cannot_be_accessed(
        self,
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

        starting_urls = [link]
        next_page_link_identifier = "table_view_collections"
        collections_base_link_identifier = "collection_details"
        destination_location = tmp_path
        file_to_be_downloaded_location = (
            Path.cwd() / "tests" / "test_data" / "test_data_main"
        )
        file_to_be_downloaded = [
            "collection1.pdf",
        ]

        # the collection_detail page won't be accessed so the year will be
        # missing from the filename
        expected_downloaded_file = [
            "Author 1_Title 1.pdf",
        ]

        run_dacoromanica_downloader(
            starting_urls=starting_urls,
            destination_folder=destination_location,
            next_page_link_identifier=next_page_link_identifier,
            collections_base_link_identifier=collections_base_link_identifier,
            get_response=test_get_link_response,
            wait=do_not_wait,
        )

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
    def test_run_application_collection_pdf_page_cannot_be_accessed(
        self,
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

        starting_urls = [link]
        next_page_link_identifier = "table_view_collections"
        collections_base_link_identifier = "collection_details"
        destination_location = tmp_path

        run_dacoromanica_downloader(
            starting_urls=starting_urls,
            destination_folder=destination_location,
            next_page_link_identifier=next_page_link_identifier,
            collections_base_link_identifier=collections_base_link_identifier,
            get_response=test_get_link_response,
            wait=do_not_wait,
        )

        out, _ = capsys.readouterr()
        assert "'Title 1' was not downloaded" in out
