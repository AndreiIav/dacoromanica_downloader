from collections import namedtuple

import pytest

from dacoromanica_downloader.download_pdf import get_link_response
from dacoromanica_downloader.main import create_CollectionPdf, generate_next_page_url
from dacoromanica_downloader.model import CollectionPdf
from dacoromanica_downloader.scrape import get_soup


@pytest.mark.parametrize("test_file", ["test_data_main/collections_page1.html"])
def test_generate_next_page_url(get_path_to_test_file, access_local_file_with_requests):
    link = get_path_to_test_file
    response = get_link_response(link, access_local_file_with_requests)
    soup = get_soup(response)

    res = generate_next_page_url(soup, next_page_link_identifier="collection_details")

    res_list = list(res)

    assert len(res_list) == 1
    assert res_list[0] == "collection_details_page1.html"


def test_create_CollectionPdf():
    CollectionInfo = namedtuple(
        "CollectionInfo", ["details_link", "title", "author", "pdf_link"]
    )
    collection_information = [
        ["details_link_1", "title_1", "author_1", "pdf_link_1"],
        ["details_link_2", "title_2", "author_2", "pdf_link_2"],
    ]
    generator = (
        CollectionInfo(details_link=i[0], title=i[1], author=i[2], pdf_link=i[3])
        for i in collection_information
    )

    res = create_CollectionPdf(generator)

    assert isinstance(res[0], CollectionPdf)
    assert isinstance(res[1], CollectionPdf)

    assert res[0].details_link == "details_link_1"
    assert res[0].title == "title_1"
    assert res[0].author == "author_1"
    assert res[0].pdf_link == "pdf_link_1"

    assert res[1].details_link == "details_link_2"
    assert res[1].title == "title_2"
    assert res[1].author == "author_2"
    assert res[1].pdf_link == "pdf_link_2"
