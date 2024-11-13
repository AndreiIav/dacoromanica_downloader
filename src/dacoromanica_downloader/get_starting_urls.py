from pathlib import Path


class EmptyFileError(Exception):
    """Raised when a file contains no data."""

    def __init__(self, name: str):
        super().__init__(f"'{name}' file contains no data. Please add data to file.")
        self.name = name


def get_starting_urls(urls_file_path: Path) -> list[str]:
    """
    Gets urls stored in a file text.

    Args:
        urls_file_path (Path): Path to the file text containing the urls.

    Returns:
        list[str]: List of urls.

    Raises:
        FileNotFoundError: If no file is found at the path.
        EmptyFileError: If the file contains no data.
    """
    if not urls_file_path.is_file():
        raise FileNotFoundError(
            f"'{str(urls_file_path)}' file does not exist."
            f" Please add a '{str(urls_file_path)}' in the"
            " 'dacoromanica_downloader' folder."
        )

    with open(urls_file_path, encoding="utf_8") as f:
        urls = f.read()

    if not urls:
        raise EmptyFileError(str(urls_file_path))

    return urls.split()
