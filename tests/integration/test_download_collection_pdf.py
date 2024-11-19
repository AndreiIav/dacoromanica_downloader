import pytest

from dacoromanica_downloader.download_pdf import (
    download_collection_pdf,
    get_link_response,
)


@pytest.mark.parametrize("test_file", ["test.pdf"])
def test_download_collection_pdf_saves_file(
    access_local_file_with_requests, get_path_to_test_file, tmp_path, capsys
):
    pdf_link = get_path_to_test_file
    pdf_name = "test_pdf_name.pdf"
    destination_folder = tmp_path
    response = get_link_response(pdf_link, get_request=access_local_file_with_requests)

    download_collection_pdf(
        response=response,
        pdf_name=pdf_name,
        destination_folder=destination_folder,
    )

    destination_path = tmp_path / pdf_name
    out, _ = capsys.readouterr()

    assert destination_path.is_file()
    assert f"'{pdf_name}' downloaded in '{destination_folder}' folder." in out


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
    response = get_link_response(pdf_link, get_request=access_local_file_with_requests)

    download_collection_pdf(
        response=response,
        pdf_name=pdf_name,
        destination_folder=destination_folder,
    )

    destination_path = tmp_path / f"{pdf_name_within_limit}{extension}"
    out, _ = capsys.readouterr()

    assert destination_path.is_file()
    assert (
        f"'{pdf_name}' file name was shortened to:"
        f" '{pdf_name_within_limit}{extension}'"
    ) in out
    assert (
        f"'{pdf_name_within_limit}{extension}' downloaded in"
        f" '{destination_folder}' folder."
    ) in out


@pytest.mark.parametrize("test_file", ["test.pdf"])
def test_download_collection_pdf_does_not_download_file_if_name_cannot_be_shortened(
    access_local_file_with_requests, get_path_to_test_file, tmp_path, capsys
):
    pdf_link = get_path_to_test_file
    destination_folder = tmp_path
    destination_folder_string_length = len(str(destination_folder))
    filename_limit = destination_folder_string_length - 10
    pdf_name = "a.pdf"
    response = get_link_response(pdf_link, get_request=access_local_file_with_requests)

    download_collection_pdf(
        response=response,
        pdf_name=pdf_name,
        destination_folder=destination_folder,
        path_length_limit=filename_limit,
    )

    destination_path = tmp_path / pdf_name
    out, _ = capsys.readouterr()

    assert (
        f"'{destination_path}' file name is too long and cannot be saved."
        " File not downloaded."
    ) in out
    assert not destination_path.is_file()


@pytest.mark.parametrize("test_file", ["test.pdf"])
def test_download_collection_pdf_does_not_download_file_if_it_is_already_downloaded(
    access_local_file_with_requests, get_path_to_test_file, tmp_path, capsys
):
    destination_folder = tmp_path
    already_existing_file = destination_folder / "test_pdf_name.pdf"
    already_existing_file_content = b"Some content"
    already_existing_file.write_bytes(already_existing_file_content)
    pdf_link = get_path_to_test_file
    pdf_name = "test_pdf_name.pdf"
    response = get_link_response(pdf_link, get_request=access_local_file_with_requests)

    download_collection_pdf(
        response=response,
        pdf_name=pdf_name,
        destination_folder=destination_folder,
    )

    out, _ = capsys.readouterr()
    assert (
        f"'{pdf_name}' already present in '{destination_folder}' folder"
        " so it will not be downloaded."
    ) in out

    file_content = (destination_folder / pdf_name).read_bytes()
    assert file_content == already_existing_file_content
