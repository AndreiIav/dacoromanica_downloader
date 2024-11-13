import time
from pathlib import Path
from typing import Iterator

import requests
from bs4 import BeautifulSoup

from dacoromanica_downloader.download_pdf import (
    download_collection_pdf,
    get_link_response,
)
from dacoromanica_downloader.get_starting_urls import get_starting_urls
from dacoromanica_downloader.model import CollectionPdf
from dacoromanica_downloader.scrape import (
    get_collection_info,
    get_collection_year,
    get_link_for_table_view,
    get_next_page_url,
    get_soup,
)

starting_urls_file_path: Path = Path("starting_urls.txt")
starting_urls: list[str] = get_starting_urls(urls_file_path=starting_urls_file_path)
next_page_link_identifier: str = "func=results-next-page&result_format=001"
collections_base_link_identifier: str = "base=GEN01"
destination_folder: Path = Path("downloaded_files")


def generate_next_page_url(
    soup: BeautifulSoup, next_page_link_identifier: str = next_page_link_identifier
) -> Iterator[str]:
    """
    Generates a next_page url if it is found in the provided BeautifulSoup
    object.

    It uses get_next_page_url() to find the url in the BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing parsed HTML.
        next_page_link_identifier (str): The name used to identify the searched
        link.

    Yields:
        str: A string containig the next_page url.
    """
    next_page = get_next_page_url(
        soup, next_page_link_identifier=next_page_link_identifier
    )
    if next_page:
        yield next_page


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


def main() -> None:
    all_collections: list[CollectionPdf] = []

    for starting_url in starting_urls:
        starting_url_response = get_link_response(link=starting_url)
        if not isinstance(starting_url_response, requests.Response):
            print(
                f"{starting_url} could not be accessed because of: "
                f"{starting_url_response}. "
                "No files can be downloaded from the link."
            )
            continue
        starting_url_soup = get_soup(response=starting_url_response)
        table_view_url = get_link_for_table_view(soup=starting_url_soup)
        if not table_view_url:
            print(
                f"{starting_url} is not a valid Dacoromanica documents page. "
                "No files can be downloaded from the link."
            )
            continue

        table_view_response = get_link_response(link=table_view_url)
        if not isinstance(table_view_response, requests.Response):
            print(
                f"the table view cannot be accessed for: {starting_url}."
                "No files can be downloaded from the link."
            )
            continue
        table_view_soup = get_soup(response=table_view_response)
        all_collections_on_page_details = get_collection_info(
            soup=table_view_soup,
            collections_base_link_identifier=collections_base_link_identifier,
        )
        all_page_collections = create_CollectionPdf(all_collections_on_page_details)
        all_collections.extend(all_page_collections)

        next_page = generate_next_page_url(
            table_view_soup, next_page_link_identifier=next_page_link_identifier
        )
        for page in next_page:
            page_response = get_link_response(link=page)
            if not isinstance(page_response, requests.Response):
                print(
                    f"{page} could not be accessed because of: {page_response}."
                    "No files can be downloaded from the link."
                )
                continue
            page_soup = get_soup(response=page_response)
            all_collections_on_page_details = get_collection_info(
                soup=page_soup,
                collections_base_link_identifier=collections_base_link_identifier,
            )
            all_page_collections = create_CollectionPdf(all_collections_on_page_details)
            all_collections.extend(all_page_collections)

    for collection in all_collections:
        year_response = get_link_response(link=collection.details_link)
        if not isinstance(year_response, requests.Response):
            continue
        year_soup = get_soup(response=year_response)
        year = get_collection_year(soup=year_soup)
        if year:
            collection.update_collection_year(year=year)
        time.sleep(1)

    sorted_collections = sorted(all_collections, key=lambda x: (x.year, x.author))

    for collection in sorted_collections:
        response = get_link_response(link=collection.pdf_link)
        if not isinstance(response, requests.Response):
            print(
                f"'{collection.title}' was not downloaded due to this error: "
                f"{response} ."
            )
            continue
        download_collection_pdf(
            response=response,
            pdf_name=collection.downloaded_file_name,
            destination_folder=destination_folder,
        )
        time.sleep(3)


if __name__ == "__main__":
    main()
