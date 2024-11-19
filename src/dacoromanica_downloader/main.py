import time
from pathlib import Path
from typing import Iterator

import requests

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
    print("dacoromanica_downloader started...")

    all_collections: list[CollectionPdf] = []

    for starting_url in starting_urls:
        print(f"Gathering data from url: '{starting_url}'...")
        starting_url_response = get_link_response(link=starting_url)
        if not isinstance(starting_url_response, requests.Response):
            print(
                f"{starting_url} could not be accessed because of: "
                f"{starting_url_response}. "
                "No files can be downloaded from this link."
            )
            continue
        starting_url_soup = get_soup(response=starting_url_response)
        table_view_url = get_link_for_table_view(soup=starting_url_soup)
        if not table_view_url:
            print(
                f"'{starting_url}' is not a valid Dacoromanica collections page. "
                "No files can be downloaded from this link."
            )
            continue

        next_page_url = table_view_url
        while next_page_url:
            response = get_link_response(link=next_page_url)
            if (
                not isinstance(response, requests.Response)
                or response.status_code != 200
            ):
                f"'{next_page_url}' could not be accessed because of: {response}. "
                "No files can be downloaded from this link."
                break
            page_soup = get_soup(response=response)
            all_collections_on_page_details = get_collection_info(
                soup=page_soup,
                collections_base_link_identifier=collections_base_link_identifier,
            )
            all_page_collections = create_CollectionPdf(all_collections_on_page_details)
            all_collections.extend(all_page_collections)
            next_page_url = get_next_page_url(
                soup=page_soup, next_page_link_identifier=next_page_link_identifier
            )
            if next_page_url is None:
                break
            time.sleep(1)

    print("Updating pdf collections date of publication...")
    for collection in all_collections:
        year_response = get_link_response(link=collection.details_link)
        if (
            not isinstance(year_response, requests.Response)
            or year_response.status_code != 200
        ):
            continue
        year_soup = get_soup(response=year_response)
        year = get_collection_year(soup=year_soup)
        if year:
            collection.update_collection_year(year=year)
        time.sleep(1)

    print(f"Number of pdf files to be downloaded: {len(all_collections)}")

    sorted_collections = sorted(all_collections, key=lambda x: (x.year, x.author))

    print("Starting downloading...")
    for collection in sorted_collections:
        response = get_link_response(link=collection.pdf_link)
        if not isinstance(response, requests.Response) or response.status_code != 200:
            print(f"'{collection.title}' was not downloaded because of: {response} .")
            continue
        download_collection_pdf(
            response=response,
            pdf_name=collection.downloaded_file_name,
            destination_folder=destination_folder,
        )
        time.sleep(2)

    print("dacoromanica_downloader finished.")


if __name__ == "__main__":
    main()  # pragma: no cover
