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


def get_link_response(
    link: str, get_request: Callable = requests.get
) -> requests.Response | str:
    """
    Retrieves the HTTP response from the provided URL or returns a string
    containing exception message if an exception occurs.

    This function attempts to fetch the HTTP response for the given URL using
    a specified HTTP GET request function, defaulting to `requests.get`. If the
    request fails due to an exception (e.g., connection errors, timeouts), the
    function returns the exception message.

    Args:
        link (str): The URL of the file to retrieve.
        get_request (callable, optional): The function to use for making the GET
        request, defaulting to `requests.get`. The function should accept a URL
        as a parameter and return a response object.

    Returns:
        requests.Response | str: The HTTP response object if the request is
        successful, otherwise a string with exception message.
    """
    try:
        response = get_request(link, timeout=20)
        return response
    except requests.exceptions.HTTPError as e:
        return f"HTTPError {e}"
    except requests.exceptions.ConnectionError as e:
        return f"ConnectionError {e}"
    except requests.exceptions.Timeout as e:
        return f"Timeout exception {e}"
    except requests.exceptions.RequestException as e:
        return f"RequestException {e}"


def shorten_filename(filename: Path, path_length_limit: int = 250) -> Path:
    """
    Shortens the given file path to comply with Windows path length limitations.

    This function reduces the length of the provided absolute file path if it
    exceeds the maximum allowable length for file paths on Windows, which is set
    to 250 characters. It achieves this by shortening the filename while
    preserving the integrity of the path. If the file path cannot be shortened
    to meet the required length, a PathTooLongError exception is raised.

    Args:
        filename (Path): The absolute file path to be shortened.
        path_length_limit (int): The accepted file path limit. Defaults to 250.

    Returns:
        Path: The shortened file path.

    Raises:
        PathTooLongError: If the file path cannot be shortened to meet the 250
        character limit.
    """

    # The limit for file names on Windows is 256 but we are setting the limit to
    # 250 characters by default
    LIMIT = path_length_limit

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
        raise PathTooLongError(str(filename))

    formated_filename = filename_parent / new_filename_name

    return formated_filename


def download_file(filename: Path, http_response: requests.Response) -> None:
    """
    Saves the content from an HTTP response to a file using the pathlib and
    requests libraries.

    This function writes the data from the provided HTTP response to the
    specified file path. The file is created at the given path, and the content
    from the response is written to it.

    Args:
        filename (Path): The file path where the content will be saved.
        http_response (requests.Response): The HTTP response object containing
        the file content.

    Returns:
        None: This function does not return any value.
    """
    filename.write_bytes(http_response.content)


def download_collection_pdf(
    pdf_link: str,
    pdf_name: str,
    destination_folder: str,
    fn_get_response: Callable[[str], requests.Response | str] = get_link_response,
    path_length_limit: int = 250,
) -> None:
    """
    Downloads a PDF from a specified URL, applies optional filename shortening,
    and saves it to a destination folder.

    This function orchestrates the download of a PDF file from a given link by
    calling a series of helper functions. It retrieves the HTTP response for the
    PDF link, then shortens the filename if needed, checks if the file already
    exists and finally saves the PDF content to the specified destination folder.

    Args:
        pdf_link (str): The URL of the PDF file to download.
        pdf_name (str): The desired name for the saved PDF file, including the
        '.pdf' extension.
        destination_folder (str): The path to the folder where the PDF file will
        be saved.
        fn_get_link_response (Callable[[str], requests.Response | str]): A
        function to fetch the HTTP response from the PDF link, returning a
        string with the exception message if an error occurs. Defaults to
        'get_link_response'.
        path_length_limit (int): The accepted file path limit. Defaults to 250.

    Returns:
        None: This function does not return any value.

    Raises:
        PathTooLongError: If the filename cannot be shortened to meet system
        path length limitations.
    """

    http_response = fn_get_response(link=pdf_link)
    if not isinstance(http_response, requests.Response):
        print(f"'{pdf_name}' was not downloaded due to this error: {http_response} .")
        return

    filename = (Path(destination_folder) / pdf_name).absolute()

    # check if the length of the path is greater than 250 characters and try to
    # shorten it if it is (the maximum path length on Windows is 256 but we
    # set the limit to 250). If it cannot be shortened don't download the file.
    if len(str(filename)) > path_length_limit:
        try:
            old_pdf_name = pdf_name
            filename = shorten_filename(
                filename=filename, path_length_limit=path_length_limit
            )
            pdf_name = filename.name
            print(f"'{old_pdf_name}' file name was shortened to: '{pdf_name}'")
        except PathTooLongError as e:
            print(e)
            return

    if filename.exists():
        print(
            f"'{pdf_name}' already present in '{destination_folder}' folder"
            " so it will not be downloaded."
        )
        return

    download_file(filename=filename, http_response=http_response)
    print(f"'{pdf_name}' downloaded in '{destination_folder}' folder.")
