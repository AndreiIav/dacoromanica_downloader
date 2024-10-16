from pathlib import Path


class EmptyFileError(Exception):
    """Raised when a file contains no data."""

    def __init__(self, name):
        super().__init__(f"'{name}' file contains no data.")
        self.name = name


def get_starting_urls(urls_file_path: str) -> list[str]:
    file_path = Path(urls_file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{urls_file_path} file does not exists.")

    with open(urls_file_path, encoding="utf_8") as f:
        urls = f.read()

    if not urls:
        raise EmptyFileError(urls_file_path)

    return urls.split()
