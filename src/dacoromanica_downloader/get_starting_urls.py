from pathlib import Path


class EmptyFileError(Exception):
    """Raised when a file contains no data."""

    def __init__(self, name: str):
        super().__init__(f"'{name}' file contains no data.")
        self.name = name


def get_starting_urls(urls_file_path: Path) -> list[str]:
    """
    Gets urls stored in a file text.

    Args:
        urls_file_path (Path): Path to the file text conatining the urls.

    Returns:
        list[str]: List of urls.

    Raises:
        FileNotFoundError: If no file is found at the path.
        EmptyFileError: If the file contains no data.
    """
    if not urls_file_path.is_file():
        raise FileNotFoundError(f"{urls_file_path} file does not exists.")

    with open(urls_file_path, encoding="utf_8") as f:
        urls = f.read()

    if not urls:
        raise EmptyFileError(urls_file_path)

    return urls.split()
