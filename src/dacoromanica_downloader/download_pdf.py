from pathlib import Path
from typing import Callable

import requests


class PathTooLongError(Exception):
    """Raised when a path is longer than 250 characters and cannot be
    shortened.
    """

    def __init__(self, filename: str) -> None:
        super().__init__(
            f"'{filename}' file name is too long and cannot be saved. File not"
            " downloaded."
        )
        self.filename = filename


def shorten_filename(filename: Path) -> tuple[Path, str]:
    """
    Shortens the given file path to comply with Windows path length limitations.

    This function reduces the length of the provided absolute file path if it
    exceeds the maximum allowable length for file paths on Windows, which is set
    to 250 characters. It achieves this by shortening the filename while
    preserving the integrity of the path. If the file path cannot be shortened
    to meet the required length, a PathTooLongError exception is raised.

    Args:
        filename (Path): The absolute file path to be shortened.

    Returns:
        tuple[Path, str]: A tuple containing the shortened file path and the
        truncated portion of the filename.

    Raises:
        PathTooLongError: If the file path cannot be shortened to meet the 250
        character limit.
    """

    # The limit for file names on Windows is 256 but we are setting the limit to
    # 250 characters
    LIMIT = 250

    # Determine by how many characters should the filename be shortened
    shortening_length = len(str(filename)) - LIMIT

    # Use Path operations to split the filename in the actual name (filename_name)
    # and the location on the filesystem (filename_parent)
    filename_path = Path(filename)
    filename_name = filename_path.name
    filename_parent = filename_path.parent

    # remove extension (".pdf") from filename_name
    filename_name_without_extension = filename_name[:-4]

    if len(filename_name_without_extension) > shortening_length:
        i = len(filename_name_without_extension) - shortening_length
        new_filename_name = filename_name_without_extension[:i] + ".pdf"
    else:
        raise PathTooLongError(filename)

    formated_filename = filename_parent / new_filename_name

    return formated_filename, new_filename_name


def download_pdf_file(
    pdf_link: str,
    pdf_name: str,
    destination_folder: str,
    shorten_filename_fn: Callable[[Path], tuple[Path, str]] = shorten_filename,
) -> None:
    """
    Downloads a PDF file from a given URL, optionally shortens the filename, and
    saves it to a specified destination.

    This function retrieves a PDF file from the provided URL and saves it with
    the specified file name in the designated folder. If the resulting file path
    exceeds length limitations, a custom filename shortening function is applied
    to ensure compliance with path length constraints. If the file already exists
    it doesn't download it again. If the download is unsuccessful or the file
    cannot be saved, appropriate exceptions are raised.

    Args:
        pdf_link (str): The URL of the PDF file to be downloaded.
        pdf_name (str): The name to save the PDF file as, including the '.pdf'
        extension.
        destination_folder (str): The path to the folder where the PDF file will
        be saved.
        shorten_filename_fn (Callable[[Path], tuple[Path, str]]): A function to
        shorten the filename if the path exceeds system limitations. Defaults to
        'shorten_filename'.

    Returns:
        None: This function does not return any value.

    Raises:
        Various exceptions may be raised if the download or file writing process
        fails, such as requests.exceptions.RequestException for network-related
        errors or IOError for file system errors.
    """
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

    filename = (Path(destination_folder) / pdf_name).absolute()

    # check if the length of the path is greater than 250 characters and try to
    # shorten it if it is (the maximum path length on Windows is 256 but we
    # set the limit to 250). If it cannot be shortened don't download the file.
    if len(str(filename)) > 250:
        try:
            old_pdf_name = pdf_name
            filename, pdf_name = shorten_filename(filename=filename)
            print(f"'{old_pdf_name}' file name was shortened to: '{pdf_name}'")
        except PathTooLongError as e:
            print(e)
            return

    if filename.exists():
        print(
            f"'{pdf_name}' already present in '{destination_folder}' folder"
            " so it will not be downloaded."
        )
    else:
        filename.write_bytes(r.content)
        print(f"'{pdf_name}' downloaded in '{destination_folder}' folder.")
