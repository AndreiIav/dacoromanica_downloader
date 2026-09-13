import argparse
from collections.abc import Iterable
from pathlib import Path

from dacoromanica_downloader.application import run_dacoromanica_downloader
from dacoromanica_downloader.get_starting_urls import get_starting_urls

NEXT_PAGE_LINK_IDENTIFIER: str = "func=results-next-page&result_format=001"
COLLECTIONS_BASE_LINK_IDENTIFIER: str = "base=GEN01"


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="dacoromanica_downloader",
        description="Downloads PDFs from Dacoromanica website.",
    )

    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="starting_urls.txt",
        help="Path to the folder containg the URLs to download from",
    )

    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        default="downloaded_files",
        help="Path to the folder where to download the files",
    )

    parser.add_argument(
        "-n",
        "--next_page_identifier",
        type=str,
        default=NEXT_PAGE_LINK_IDENTIFIER,
        help="The name used to identify next page when parsing a page",
    )

    parser.add_argument(
        "-c",
        "--collections_identifier",
        type=str,
        default=COLLECTIONS_BASE_LINK_IDENTIFIER,
        help="The name used to identify a collection parsing a page",
    )

    return parser


def main(argv: Iterable[str] | None = None) -> int:

    parser = build_parser()
    args = parser.parse_args(argv)

    starting_urls = get_starting_urls(urls_file_path=Path(args.source))
    run_dacoromanica_downloader(
        starting_urls=starting_urls,
        destination_folder=Path(args.destination),
        next_page_link_identifier=args.next_page_identifier,
        collections_base_link_identifier=args.collections_identifier,
    )

    return 0
