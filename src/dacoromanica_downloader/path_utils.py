from pathlib import Path

from dacoromanica_downloader.custom_exceptions import EmptyFileError, PathTooLongError


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
            f"'{urls_file_path}' file does not exist."
            f" Please add a '{urls_file_path}' in the"
            " 'dacoromanica_downloader' folder."
        )

    with open(urls_file_path, encoding="utf_8") as f:
        urls = f.read()

    if not urls:
        raise EmptyFileError(str(urls_file_path))

    return urls.split()


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

    # Use Path operations to split the filename in the actual name (filename_name),
    # the location on the filesystem (filename_parent) and the extension (filename_extension)
    filename_path = Path(filename)
    filename_name = filename_path.stem
    filename_parent = filename_path.parent
    filename_extension = filename_path.suffix

    if len(filename_name) > shortening_length:
        i = len(filename_name) - shortening_length
        new_filename_name = filename_name[:i] + filename_extension
    else:
        raise PathTooLongError(str(filename))

    formated_filename = filename_parent / new_filename_name

    return formated_filename


def get_file_destination_path(
    file_name: str,
    destination_folder: Path,
    path_length_limit: int = 250,
) -> Path | None:
    """
    Constructs a destination file path, shortening the filename if necessary.

    Ensures that the destination folder exists and constructs an absolute path
    for the specified file. If the resulting path exceeds the specified length
    limit, attempts to shorten the filename to fit within the limit.

    If the filename cannot be shortened or the destination file already exists,
    the function returns None.

    Args:
        file_name (str): The desired file name, including its extension.
        destination_folder (Path): The folder where the file will be saved.
        path_length_limit (int): The maximum allowed file path length.
            Defaults to 250.

    Returns:
        Path | None: The resolved destination file path, or None if the path
        cannot be shortened or the file already exists.
    """
    destination_folder.mkdir(parents=True, exist_ok=True)
    filename = (destination_folder / file_name).resolve()

    # check if the length of the path is greater than 250 characters and try to
    # shorten it if it is (the maximum path length on Windows is 256 but we
    # set the limit to 250). If it cannot be shortened don't download the file.
    if len(str(filename)) > path_length_limit:
        try:
            old_pdf_name = file_name
            filename = shorten_filename(
                filename=filename, path_length_limit=path_length_limit
            )
            file_name = filename.name
            print(f"'{old_pdf_name}' file name was shortened to: '{file_name}'")
        except PathTooLongError as e:
            print(e)
            return None

    if filename.exists():
        print(
            f"'{file_name}' already present in '{destination_folder.absolute()}'"
            f" folder so it will not be downloaded."
        )
        return None

    return filename
