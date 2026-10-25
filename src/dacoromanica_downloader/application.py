import time
from collections.abc import Callable, Iterator
from pathlib import Path

import requests

from dacoromanica_downloader.custom_exceptions import NoFileToDownload
from dacoromanica_downloader.http_client import HttpClient
from dacoromanica_downloader.model import CollectionPdf
from dacoromanica_downloader.path_utils import get_file_destination_path
from dacoromanica_downloader.scrape import (
    get_collection_info,
    get_collection_year,
    get_link_for_table_view,
    get_next_page_url,
    get_soup,
)

DEFAULT_NEXT_PAGE_LINK_IDENTIFIER = "func=results-next-page&result_format=001"
DEFAULT_COLLECTIONS_BASE_LINK_IDENTIFIER = "base=GEN01"

WaitFunction = Callable[[float], None]

http_client = HttpClient()


def create_CollectionPdf(
    all_collections_on_page_details: Iterator,
) -> list[CollectionPdf]:
    """
    Creates CollectionPdf objects.

    This function creates CollectionPdf objects from a namedtuple and returns a
    list of all CollectionPdf that can be created from the information extracted
    from a target web page.

    Args:
        all_collections_on_page_details (Iterator): A generator object that
        yields a namedtuple containg data used to instantiate a CollectionPdf
        object.

    Returns:
        list: A list of CollectionPdf objects.
    """
    all_page_collections = []

    for collection_details in all_collections_on_page_details:
        new_collection = CollectionPdf(
            details_link=collection_details.details_link,
            title=collection_details.title,
            pdf_link=collection_details.pdf_link,
            author=collection_details.author,
        )
        all_page_collections.append(new_collection)

    return all_page_collections


def run_dacoromanica_downloader(
    starting_urls: list[str],
    destination_folder: Path,
    http_client: HttpClient = http_client,
    next_page_link_identifier: str = DEFAULT_NEXT_PAGE_LINK_IDENTIFIER,
    collections_base_link_identifier: str = DEFAULT_COLLECTIONS_BASE_LINK_IDENTIFIER,
    wait: WaitFunction = time.sleep,
) -> None:

    print("dacoromanica_downloader started...")

    all_collections: list[CollectionPdf] = []

    with http_client as client:
        for starting_url in starting_urls:
            print(f"Gathering data from url: '{starting_url}'...")
            try:
                starting_url_response = client.get_page(url=starting_url)
            except requests.RequestException as e:
                print(f"{starting_url} could not be accessed: {e}")
                continue
            starting_url_soup = get_soup(response=starting_url_response)
            table_view_url = get_link_for_table_view(soup=starting_url_soup)
            if not table_view_url:
                print(
                    f"'{starting_url}' is not a valid Dacoromanica collections "
                    "page. No files can be downloaded from this link."
                )
                continue

            next_page_url: str | None = table_view_url
            while next_page_url:
                try:
                    wait(1)
                    response = client.get_page(url=next_page_url)
                except requests.RequestException as e:
                    print(f"{next_page_url} page response error: {e}")
                    break

                page_soup = get_soup(response=response)
                all_collections_on_page_details = get_collection_info(
                    soup=page_soup,
                    collections_base_link_identifier=collections_base_link_identifier,
                )
                all_page_collections = create_CollectionPdf(
                    all_collections_on_page_details
                )
                all_collections.extend(all_page_collections)
                next_page_url = get_next_page_url(
                    soup=page_soup, next_page_link_identifier=next_page_link_identifier
                )
                wait(2)

        print(f"Number of pdf files to be downloaded: {len(all_collections)}")
        if len(all_collections) == 0:
            raise NoFileToDownload

        print("Updating pdf collections date of publication...")
        for collection in all_collections:
            try:
                year_response = client.get_page(url=collection.details_link)
            except requests.RequestException as e:
                print(f"Cannot access {collection} collection year response: {e}")
                continue
            year_soup = get_soup(response=year_response)
            year = get_collection_year(soup=year_soup)
            if year:
                collection.update_collection_year(year=year)
            wait(1)

        sorted_collections = sorted(all_collections, key=lambda x: (x.year, x.author))

        print("Starting downloading...")
        for collection in sorted_collections:
            file_path = get_file_destination_path(
                file_name=collection.downloaded_file_name,
                destination_folder=destination_folder,
            )
            if not file_path:
                continue
            try:
                client.download_file(url=collection.pdf_link, file_path=file_path)
            except requests.RequestException as e:
                print(f"'{collection.downloaded_file_name}' not downloaded: {e}")
                continue
            print(
                f"'{collection.downloaded_file_name}' downloaded in "
                f"'{destination_folder.absolute()}' folder."
            )
            wait(2)

    print("dacoromanica_downloader finished.")
