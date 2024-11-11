from pathlib import Path

import pytest
import requests

from dacoromanica_downloader.download_pdf import get_link_response
from dacoromanica_downloader.main import (
    generate_next_page_url,
    get_page_collections,
    main,
)
from dacoromanica_downloader.scrape import get_collection_info, get_soup


@pytest.mark.parametrize("test_file", ["test_data_main/collections_page1.html"])
def test_generate_next_page_url(get_path_to_test_file, access_local_file_with_requests):
    link = get_path_to_test_file
    response = get_link_response(link, access_local_file_with_requests)
    soup = get_soup(response)

    res = generate_next_page_url(soup, next_page_link_identifier="collection_details")

    res_list = list(res)

    assert len(res_list) == 1
    assert res_list[0] == "collection_details_page1.html"


@pytest.mark.parametrize("test_file", ["test_data_main/table_view_collections1.html"])
def test_get_page_collections(get_path_to_test_file, access_local_file_with_requests):
    link = get_path_to_test_file
    response = get_link_response(link, access_local_file_with_requests)
    soup = get_soup(response)
    all_collections_on_page_details = get_collection_info(
        soup, collections_base_link_identifier="collection_details"
    )

    res = get_page_collections(all_collections_on_page_details)

    assert len(res) == 2


@pytest.mark.parametrize("test_file", ["test_data_main/collections_page1.html"])
def test_main_end_to_end(
    monkeypatch, get_path_to_test_file, access_local_file_with_requests
):
    def new_get_link_response(link, get_request=access_local_file_with_requests):
        """
        Version of get_link_response() that works with local html files.
        Needed for making accessing local html files from relative paths work.
        """
        if "file://" not in link:
            link_path = (
                Path(".").resolve() / "tests" / "test_data" / "test_data_main" / link
            )
            link = "file://" + str(link_path)
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

    monkeypatch.setattr(
        "dacoromanica_downloader.main.get_link_response",
        new_get_link_response,
    )

    link = get_path_to_test_file
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

    res = main()

    assert len(res) == 3
