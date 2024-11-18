from collections import namedtuple

from dacoromanica_downloader.main import create_CollectionPdf
from dacoromanica_downloader.model import CollectionPdf


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
