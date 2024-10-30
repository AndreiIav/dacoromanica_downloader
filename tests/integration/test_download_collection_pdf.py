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


# TODO
def test_download_collection_pdf_does_not_download_file_if_http_exception_is_raised():
    pass


@pytest.mark.parametrize("test_file", ["test.pdf"])
def test_download_collection_pdf_shortens_pdf_name_that_is_over_limit_and_saves_file(
    access_local_file_with_requests, get_path_to_test_file, tmp_path, capsys
):
    pdf_link = get_path_to_test_file
    destination_folder = tmp_path
    filename_limit = 250
    # add 1 to adjust for the / added between path and file name when the full
    # pathname will be resolved
    destination_folder_string_length = len(str(destination_folder)) + 1
    extension = ".pdf"
    diff_until_limit = filename_limit - (
        destination_folder_string_length + len(extension)
    )
    pdf_name_within_limit = "a" * diff_until_limit
    pdf_name_over_limit = "b" * 5
    pdf_name = f"{pdf_name_within_limit}{pdf_name_over_limit}{extension}"

    new_fn_get_link_response = partial(
        get_link_response, get_request=access_local_file_with_requests
    )

    download_collection_pdf(
        pdf_link=pdf_link,
        pdf_name=pdf_name,
        destination_folder=destination_folder,
        fn_get_response=new_fn_get_link_response,
    )

    destination_path = tmp_path / f"{pdf_name_within_limit}{extension}"
    out, _ = capsys.readouterr()

    assert destination_path.is_file()
    assert (
        f"'{pdf_name}' file name was shortened to: '{pdf_name_within_limit}{extension}'"
    ) in out
    assert (
        f"'{pdf_name_within_limit}{extension}' downloaded in '{destination_folder}' folder."
        in out
    )


# TODO
def test_download_collection_pdf_does_not_download_file_if_name_cannot_be_shortened():
    pass


def test_download_collection_pdf_does_not_download_file_if_it_is_already_downloaded():
    pass
