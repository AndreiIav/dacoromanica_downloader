from pathlib import Path

import pytest

from dacoromanica_downloader.path_utils import (
    EmptyFileError,
    PathTooLongError,
    get_file_destination_path,
    get_starting_urls,
    shorten_filename,
)


class TestGetStartingUrls:
    def test_get_starting_urls_gets_urls(self, tmp_path):
        file_location = tmp_path / "test_file_urls.txt"
        with open(file_location, "a", encoding="utf_8") as f:
            f.write("link_1\n")
            f.write("link_2 ")
            f.write("link_3")

        res = get_starting_urls(file_location)

        assert res == ["link_1", "link_2", "link_3"]

    def test_get_starting_urls_raises_FileNotFoundError(self, tmp_path):
        with pytest.raises(FileNotFoundError) as err:
            get_starting_urls(tmp_path)

        assert str(err.value) == (
            f"'{tmp_path}' file does not exist."
            f" Please add a '{tmp_path}' in the"
            " 'dacoromanica_downloader' folder."
        )

    def test_get_starting_urls_raises_EmptyFileError(self, tmp_path):
        file_location = tmp_path / "test_file_urls.txt"
        file_location.touch()

        with pytest.raises(EmptyFileError) as err:
            get_starting_urls(file_location)

        assert (
            str(err.value)
            == f"'{file_location}' file contains no data. Please add data to file."
        )


class TestShortenFilename:
    def test_shorten_filename_shortens_filename_that_is_over_limit(self):
        limit = 250
        extension = ".pdf"  # 4 characters
        # 5 characters + 1 for the slash that will be added when the path will be resolved
        path = "h" * 5
        file_name_within_limit = "a" * 240
        file_name_over_limit = "b" * 5
        filename = (
            Path(path) / f"{file_name_within_limit}{file_name_over_limit}{extension}"
        )

        formated_filename = shorten_filename(filename)

        assert len(str(formated_filename)) == limit
        assert str(formated_filename) == str(
            Path(path) / f"{file_name_within_limit}{extension}"
        )

    def test_shorten_filename_does_not_shorten_name_that_is_not_over_limit(self):
        limit = 250
        extension = ".pdf"  # 4 characters
        # 5 characters + 1 for the slash that will be added when the path will be resolved
        path = "h" * 5
        file_name_within_limit = "a" * 240
        filename = Path(path) / f"{file_name_within_limit}{extension}"

        formated_filename = shorten_filename(filename)

        assert len(str(formated_filename)) == limit
        assert str(formated_filename) == str(
            Path(path) / f"{file_name_within_limit}{extension}"
        )

    def test_shorten_filename_raises_exception_if_filename_can_not_be_shortened(self):
        extension = ".pdf"  # 4 characters
        # 249 characters + 1 for the slash that will be added when the path will be resolved
        path = "h" * 249
        file_name = "a" * 10
        # filename = f"{path}{file_name}{extension}"
        filename = Path(path) / f"{path}{file_name}{extension}"

        with pytest.raises(PathTooLongError) as e:
            shorten_filename(filename)

        assert (
            f"'{filename}' file name is too long and cannot be saved."
            " File not downloaded." in str(e.value)
        )


class TestGetFileDestinationPath:
    def test_get_file_destination_path_creates_destination_directory(
        self,
        tmp_path,
    ):
        file_name = "test.pdf"
        destination = tmp_path / "nested" / "downloads"

        get_file_destination_path(file_name=file_name, destination_folder=destination)

        assert destination.is_dir()

    def test_get_file_destination_path_returns_file_path(self, tmp_path):
        file_name = "test.pdf"
        destination = tmp_path / "downloads"

        file_path = get_file_destination_path(
            file_name=file_name, destination_folder=destination
        )

        assert file_path == destination / file_name

    def test_get_file_destination_path_shortens_file_path(self, tmp_path):
        destination = tmp_path / "downloads"
        path_length_limit = 250
        over_the_limit = 10
        file_name = "a" * ((path_length_limit - len(str(destination))) + over_the_limit)

        file_path = get_file_destination_path(
            file_name=file_name,
            destination_folder=destination,
            path_length_limit=path_length_limit,
        )

        assert len(str(file_path)) == 250

    def test_get_file_destination_path_returns_none_when_file_already_exists(
        self, tmp_path, capsys
    ):
        file_name = "file.txt"
        destination = tmp_path / "downloads"
        destination.mkdir()
        destination_file = destination / file_name
        destination_file.write_text("data")

        file_path = get_file_destination_path(
            file_name=file_name,
            destination_folder=destination,
        )

        out, _ = capsys.readouterr()
        assert file_path is None
        assert (
            f"'{file_name}' already present in '{destination.absolute()}'"
            f" folder so it will not be downloaded."
        ) in out
