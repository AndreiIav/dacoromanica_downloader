from functools import partial

import pytest

from dacoromanica_downloader.download_pdf import (
    download_collection_pdf,
    get_link_response,
)


@pytest.mark.parametrize("test_file", ["test.pdf"])
def test_download_collection_pdf(
    access_local_file_with_requests, get_path_to_test_file, tmp_path, capsys
):
    pdf_link = get_path_to_test_file
    pdf_name = "test_pdf_name.pdf"
    destination_folder = tmp_path
    new_fn_get_link_response = partial(
        get_link_response, get_request=access_local_file_with_requests
    )

    download_collection_pdf(
        pdf_link=pdf_link,
        pdf_name=pdf_name,
        destination_folder=destination_folder,
        fn_get_response=new_fn_get_link_response,
    )

    destination_path = tmp_path / pdf_name
    out, _ = capsys.readouterr()

    assert destination_path.is_file()
    assert f"'{pdf_name}' downloaded in '{destination_folder}' folder." in out
