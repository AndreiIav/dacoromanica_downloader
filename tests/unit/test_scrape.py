from functools import partial

import pytest
from bs4 import BeautifulSoup

from dacoromanica_downloader.download_pdf import get_link_response
from dacoromanica_downloader.scrape import get_soup


class TestGetSoup:
    @pytest.mark.parametrize("test_file", ["test_page.html"])
    def test_get_soup_gets_soup(
        self, access_local_file_with_requests, get_path_to_test_file
    ):
        link = get_path_to_test_file
        new_fn_get_link_response = partial(
            get_link_response, get_request=access_local_file_with_requests
        )

        get_soup_value = get_soup(link, new_fn_get_link_response)

        assert isinstance(get_soup_value, BeautifulSoup)

    def test_get_soup_returns_error_message_when_error_occures(self):
        link = "link"

        get_soup_value = get_soup(link)

        assert isinstance(get_soup_value, str)
        assert "RequestException" in get_soup_value
