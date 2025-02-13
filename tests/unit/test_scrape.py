import pytest
from bs4 import BeautifulSoup

from dacoromanica_downloader.download_pdf import get_link_response
from dacoromanica_downloader.scrape import (
    get_collection_info,
    get_collection_year,
    get_link_for_table_view,
    get_next_page_url,
    get_soup,
)


class TestGetSoup:
    @pytest.mark.parametrize("test_file", ["test_page.html"])
    def test_get_soup_gets_soup(
        self, access_local_file_with_requests, get_path_to_test_file
    ):
        link = get_path_to_test_file
        response = get_link_response(link, access_local_file_with_requests)

        soup = get_soup(response)

        assert isinstance(soup, BeautifulSoup)

    @pytest.mark.parametrize("test_file", ["test_page.html"])
    def test_get_soup_contains_correct_data(
        self, access_local_file_with_requests, get_path_to_test_file
    ):
        link = get_path_to_test_file
        response = get_link_response(link, access_local_file_with_requests)

        soup = get_soup(response)

        assert soup.find("h1").string == "vânătoare bărbați pietriș"
        assert soup.find("p").string == "VÂNĂTOARE BĂRBAȚI PIETRIȘ"


class TestGetNextPageUrl:
    @pytest.mark.parametrize("test_file", ["test_get_next_page_url.html"])
    def test_get_next_page_url_gets_url(
        self, access_local_file_with_requests, get_path_to_test_file
    ):
        link = get_path_to_test_file
        response = get_link_response(link, access_local_file_with_requests)
        soup = get_soup(response)
        next_page_link_identifier = "func=results-next-page&result_format=001"

        res = get_next_page_url(
            soup, next_page_link_identifier=next_page_link_identifier
        )

        assert res == "nextPageLinkfunc=results-next-page&result_format=001"

    @pytest.mark.parametrize("test_file", ["test_page.html"])
    def test_get_next_page_url_returns_None_if_url_not_found(
        self, access_local_file_with_requests, get_path_to_test_file
    ):
        link = get_path_to_test_file
        response = get_link_response(link, access_local_file_with_requests)
        soup = get_soup(response)
        next_page_link_identifier = "func=results-next-page&result_format=001"

        res = get_next_page_url(soup, next_page_link_identifier)

        assert res is None


class TestGetCollectionInfo:
    @pytest.mark.parametrize("test_file", ["test_get_collection_info.html"])
    def test_get_collection_info_gets_collection_info(
        self, access_local_file_with_requests, get_path_to_test_file
    ):
        link = get_path_to_test_file
        response = get_link_response(link, access_local_file_with_requests)
        soup = get_soup(response)

        # get_collection_info is a generator function so we cast its results
        # to a list to easily test the returned values
        results = list(
            get_collection_info(soup, collections_base_link_identifier="base=GEN01")
        )

        assert len(results) == 3

        assert results[0].details_link == "details.php?base=GEN01&id=1"
        assert results[0].title == "Title 1"
        assert results[0].author == "Author 1"
        assert results[0].pdf_link == "pdfs/doc1.pdf"

        assert results[1].details_link == "details.php?base=GEN01&id=2"
        assert results[1].title == "Title 2"
        assert results[1].author == ""
        assert results[1].pdf_link == "pdfs/doc2.pdf"

        assert results[2].details_link == "details.php?base=GEN01&id=3"
        assert results[2].title == "Title 3"
        assert results[2].author == "Author 3"
        assert results[2].pdf_link == "pdfs/doc3.pdf"


class TestGetCollectionYear:
    @pytest.mark.parametrize("test_file", ["test_get_collection_year.html"])
    def test_get_collection_year_gets_year(
        self, get_path_to_test_file, access_local_file_with_requests
    ):
        link = get_path_to_test_file
        response = get_link_response(link, access_local_file_with_requests)
        soup = get_soup(response)

        res = get_collection_year(soup)

        assert res == "2023"

    @pytest.mark.parametrize("test_file", ["test_page.html"])
    def test_get_collection_year_returns_None_if_year_is_not_found(
        self, get_path_to_test_file, access_local_file_with_requests
    ):
        link = get_path_to_test_file
        response = get_link_response(link, access_local_file_with_requests)
        soup = get_soup(response)

        res = get_collection_year(soup)

        assert res is None


class TestGetLinkForTableView:
    @pytest.mark.parametrize("test_file", ["test_get_link_for_table_view.html"])
    def test_get_link_for_table_view_gets_link(
        self, get_path_to_test_file, access_local_file_with_requests
    ):
        link = get_path_to_test_file
        response = get_link_response(link, access_local_file_with_requests)
        soup = get_soup(response)

        res = get_link_for_table_view(soup)

        assert res == "table_view_link.html"

    @pytest.mark.parametrize("test_file", ["test_page.html"])
    def test_get_link_for_table_view_returns_None_if_link_not_found(
        self, get_path_to_test_file, access_local_file_with_requests
    ):
        link = get_path_to_test_file
        response = get_link_response(link, access_local_file_with_requests)
        soup = get_soup(response)

        res = get_link_for_table_view(soup)

        assert res is None
