import pytest

from dacoromanica_downloader.model import CollectionPdf


class TestCollectionPdf:
    def test_CollectionPdf_repr(self):
        details_link = "details_link"
        title = "title"
        author = "author"
        year = 1989
        test_collection = CollectionPdf(
            details_link=details_link,
            title=title,
            pdf_link="pdf_link",
            author=author,
            year=1989,
        )

        assert repr(test_collection) == f"CollectionPdf({details_link},{title},{year})"

    def test_CollectionPdf_str(self):
        title = "title"
        author = "author"
        year = 1989
        test_collection = CollectionPdf(
            details_link="details_link",
            title=title,
            pdf_link="pdf_link",
            author=author,
            year=1989,
        )

        assert str(test_collection) == f"title: {title}, author: {author}, year: {year}"

    def test_CollectionPdf_gt(self):
        all_collections = []

        collection_1 = CollectionPdf(
            details_link="details_link",
            title="title",
            pdf_link="pdf_link",
            author="author",
            year=1900,
        )
        all_collections.append(collection_1)

        collection_2 = CollectionPdf(
            details_link="details_link",
            title="title",
            pdf_link="pdf_link",
            author="author",
        )
        all_collections.append(collection_2)

        collection_3 = CollectionPdf(
            details_link="details_link",
            title="title",
            pdf_link="pdf_link",
            author="author",
            year=1899,
        )
        all_collections.append(collection_3)

        all_collections.sort()

        assert all_collections[0] == collection_2
        assert all_collections[1] == collection_3
        assert all_collections[2] == collection_1


class TestCollectionPdfUpdateCollectionYear:
    @pytest.mark.parametrize("input, expected_result", [("1", 1), ("9999", 9999)])
    def test_update_collection_year_updates_year_when_valid_year_is_provided(
        self, input, expected_result
    ):
        test_collection = CollectionPdf(
            details_link="details_link",
            title="title",
            pdf_link="pdf_link",
            author="author",
        )

        test_collection.update_collection_year(year=input)

        assert test_collection.year == expected_result

    @pytest.mark.parametrize(
        "input, expected_result",
        [("19999", 1999), ("[188888]", 1888), ("year 2 BC", 2)],
    )
    def test_update_collection_year_updates_year_when_a_valid_year_can_be_extracted(
        self, input, expected_result
    ):
        test_collection = CollectionPdf(
            details_link="details_link",
            title="title",
            pdf_link="pdf_link",
            author="author",
        )

        test_collection.update_collection_year(year=input)

        assert test_collection.year == expected_result

    @pytest.mark.parametrize("input", ["", "year"])
    def test_update_collection_year_does_not_update_year_when_invalid_year_is_provided(
        self, input
    ):
        test_collection = CollectionPdf(
            details_link="details_link",
            title="title",
            pdf_link="pdf_link",
            author="author",
        )

        test_collection.update_collection_year(year=input)

        assert test_collection.year == 0


class TestCollectionPdfDownloadedFileName:
    def test_downloaded_file_name_is_author_title_year(self):
        title = "title"
        author = "author"
        year = 1989
        test_collection = CollectionPdf(
            details_link="details_link",
            title=title,
            pdf_link="pdf_link",
            author=author,
            year=year,
        )

        assert test_collection.downloaded_file_name == f"{author}_{title}_{year}.pdf"

    def test_downloaded_file_name_is_title_year(self):
        title = "title"
        year = 1989

        test_collection = CollectionPdf(
            details_link="details_link",
            title=title,
            pdf_link="pdf_link",
            year=year,
        )

        assert test_collection.downloaded_file_name == f"{title}_{year}.pdf"

    def test_downloaded_file_name_is_author_title(self):
        title = "title"
        author = "author"

        test_collection = CollectionPdf(
            details_link="details_link",
            title=title,
            pdf_link="pdf_link",
            author=author,
        )

        assert test_collection.downloaded_file_name == f"{author}_{title}.pdf"

    def test_downloaded_file_name_is_title(self):
        title = "title"

        test_collection = CollectionPdf(
            details_link="details_link",
            title=title,
            pdf_link="pdf_link",
        )

        assert test_collection.downloaded_file_name == f"{title}.pdf"

    def test_downloaded_file_name_removes_forbidden_charactes_from_title_and_author(
        self,
    ):
        forbiden_characters = "<>:'\"/'\\|/?*"
        title = "title"
        author = "author"

        test_collection = CollectionPdf(
            details_link="details_link",
            title=f"{title}{forbiden_characters}",
            pdf_link="pdf_link",
            author=f"{author}{forbiden_characters}",
        )

        assert test_collection.downloaded_file_name == f"{author}_{title}.pdf"
