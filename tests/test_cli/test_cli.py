import pytest

from dacoromanica_downloader.cli import main


@pytest.mark.parametrize("test_file", ["test_data_main/collections_page1.html"])
def test_cli_works(get_path_to_test_file, tmp_path, capsys):
    source = get_path_to_test_file
    destination = str(tmp_path)
    next_page_identifier = "table_view_collections"
    collections_identifier = "collection_details"

    # print(f"urls_file_path is {urls_file_path}_type{type(urls_file_path)}")

    args = {
        "source": source,
        "destination": destination,
        "next_page_identifier": next_page_identifier,
        "collections_identifier": collections_identifier,
    }

    # print(f"args is {args}")

    main(args)

    captured = capsys.readouterr()

    assert "dacoromanica_downloader finished." in captured.out
