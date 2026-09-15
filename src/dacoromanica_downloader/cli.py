import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from dacoromanica_downloader.application import run_dacoromanica_downloader
from dacoromanica_downloader.get_starting_urls import get_starting_urls


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="dacoromanica_downloader",
        description="Download PDFs from Dacoromanica website.",
    )

    parser.add_argument(
        "-s",
        "--source",
        type=Path,
        default=Path("starting_urls.txt"),
        help="Path to the text file containing the starting URLs.",
    )

    parser.add_argument(
        "-d",
        "--destination",
        type=Path,
        default=Path("downloaded_files"),
        help="Directory where downloaded PDF files will be saved.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:

    parser = build_parser()
    arguments = parser.parse_args(argv)

    try:
        starting_urls = get_starting_urls(urls_file_path=arguments.source)
        run_dacoromanica_downloader(
            starting_urls=starting_urls,
            destination_folder=arguments.destination,
        )
    except OSError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0
