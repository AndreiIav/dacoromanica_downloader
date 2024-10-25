import pytest

from dacoromanica_downloader.download_pdf import PathTooLongError, shorten_filename


class TestShortenFilename:
    def test_shorten_filename_shortens_filename_that_is_over_limit(self):
        limit = 250
        extension = ".pdf"  # 4 characters
        path = ("h" * 5) + "/"  # 6 characters
        file_name_within_limit = "a" * 240
        file_name_over_limit = "b" * 5
        filename = f"{path}{file_name_within_limit}{file_name_over_limit}{extension}"

        formated_filename = shorten_filename(filename)

        assert len(str(formated_filename)) == limit
        assert str(formated_filename) == f"{path}{file_name_within_limit}{extension}"

    def test_shorten_filename_does_not_shorten_name_that_is_not_over_limit(self):
        limit = 250
        extension = ".pdf"  # 4 characters
        path = ("h" * 5) + "/"  # 6 characters
        file_name_within_limit = "a" * 240
        filename = f"{path}{file_name_within_limit}{extension}"

        formated_filename = shorten_filename(filename)

        assert len(str(formated_filename)) == limit
        assert str(formated_filename) == f"{path}{file_name_within_limit}{extension}"

    def test_shorten_filename_raises_exception_if_filename_can_not_be_shortened(self):
        extension = ".pdf"  # 4 characters
        path = ("h" * 249) + "/"  # 250 charactes
        file_name = "a" * 10
        filename = f"{path}{file_name}{extension}"

        with pytest.raises(PathTooLongError) as e:
            shorten_filename(filename)

        assert (
            f"'{filename}' file name is too long and cannot be saved."
            " File not downloaded." in str(e.value)
        )
