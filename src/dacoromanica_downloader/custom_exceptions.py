class NoFileToDownload(Exception):
    """Raised when there is no file to be downloaded."""

    def __init__(self) -> None:
        super().__init__("No file to download.")


class PathTooLongError(Exception):
    """Raised when a path is longer than 250 characters and cannot be shortened."""

    def __init__(self, filename: str) -> None:
        super().__init__(
            f"'{filename}' file name is too long and cannot be saved. File not"
            " downloaded."
        )
        self.filename = filename


class EmptyFileError(Exception):
    """Raised when a file contains no data."""

    def __init__(self, name: str):
        super().__init__(f"'{name}' file contains no data. Please add data to file.")
        self.name = name
