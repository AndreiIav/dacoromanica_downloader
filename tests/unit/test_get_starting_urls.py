import pytest

from dacoromanica_downloader.get_starting_urls import EmptyFileError, get_starting_urls


def test_get_starting_urls_gets_urls(tmp_path):
    file_location = tmp_path / "test_file_urls.txt"
    with open(file_location, "a", encoding="utf_8") as f:
        f.write("link_1\n")
        f.write("link_2 ")
        f.write("link_3")

    res = get_starting_urls(file_location)

    assert res == ["link_1", "link_2", "link_3"]


def test_get_starting_urls_raises_FileNotFoundError(tmp_path):
    with pytest.raises(FileNotFoundError) as err:
        get_starting_urls(tmp_path)

    assert str(err.value) == (
        f"'{str(tmp_path)}' file does not exist."
        f" Please add a '{str(tmp_path)}' in the"
        " 'dacoromanica_downloader' folder."
    )


def test_get_starting_urls_raises_EmptyFileError(tmp_path):
    file_location = tmp_path / "test_file_urls.txt"
    file_location.touch()

    with pytest.raises(EmptyFileError) as err:
        get_starting_urls(file_location)

    assert (
        str(err.value)
        == f"'{file_location}' file contains no data. Please add data to file."
    )
