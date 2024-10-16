from pathlib import Path

import requests


class PathTooLongError(Exception):
    """Raised when a path is longer than 260 characters and cannot be
    shortened.
    """

    def __init__(self, filename):
        super().__init__(
            f"'{filename}' file name is too long and cannot be saved. File not"
            " downloaded."
        )
        self.filename = filename


def download_pdf_file(pdf_link: str, pdf_name: str, destination_folder: str) -> None:
    try:
        r = requests.get(pdf_link, stream=True)
    except requests.exceptions.HTTPError as e:
        print(
            f"'{pdf_name}' file not downloaded. The following exception occurred: {e}"
        )
        return
    except requests.exceptions.ConnectionError as e:
        print(
            f"'{pdf_name}' file not downloaded. The following exception occurred: {e}"
        )
        return
    except requests.exceptions.Timeout as e:
        print(
            f"'{pdf_name}' file not downloaded. The following exception occurred: {e}"
        )
        return
    except requests.exceptions.RequestException as e:
        print(
            f"'{pdf_name}' file not downloaded. The following exception occurred: {e}"
        )
        return

    filename = Path(destination_folder) / pdf_name

    try:
        if filename.exists():
            print(
                f"'{pdf_name}' already present in '{destination_folder}' folder "
                " so will not be downloaded."
            )
        else:
            filename.write_bytes(r.content)
            print(f"'{pdf_name}' downloaded in '{destination_folder}' folder.")
    except OSError as e:
        if "File name too long" in e.strerror:
            try:
                shortening_length, shortened_filename, shortend_pdf_name = (
                    shorten_filename(filename)
                )
                print(
                    f"{str(filename)} file name was shortened by"
                    f" {shortening_length} characters becuase it was too long."
                )
                shortened_filename_path = Path(shortened_filename)
                shortened_filename_path.write_bytes(r.content)
                print(
                    f"'{shortend_pdf_name}' downloaded in"
                    f" '{destination_folder}' folder."
                )
            except PathTooLongError as e:
                print(e)


def shorten_filename(filename):
    # The limit for file names on Windows is 260
    limit = 260

    # Determine by how many characters should the filename be shortened
    shortening_length = len(str(filename)) - limit

    # Use Path operations to split the filename in the actual name and the
    # location on the filesystem (parent)
    filename_path = Path(filename)
    filename_name = filename_path.name
    filename_parent = filename_path.parent

    # remove extension (".pdf") from filename_name
    filename_name_without_extension = filename_name[:-4]

    if len(filename_name_without_extension) > (shortening_length + 4):
        i = len(filename_name_without_extension) - (shortening_length + 4)
        title = filename_name_without_extension[:i]
    else:
        raise PathTooLongError(filename)

    formated_filename = str(filename_parent / Path(title + ".pdf"))

    return shortening_length, formated_filename, title + ".pdf"
