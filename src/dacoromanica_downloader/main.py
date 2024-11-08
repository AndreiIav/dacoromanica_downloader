import time

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

starting_urls_file_path: str = "starting_urls.txt"
starting_urls: list[str] = get_starting_urls(urls_file_path=starting_urls_file_path)
next_page_link_identifier: str = "func=results-next-page&result_format=001"
collections_base_link_identifier: str = "base=GEN01"


def generate_next_page_url(soup, next_page_link_identifier=next_page_link_identifier):
    next_page = get_next_page_url(
        soup, next_page_link_identifier=next_page_link_identifier
    )
    if next_page:
        yield next_page


def get_page_collections(all_collections_on_page_details):
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


def main():
    all_collections = []

    for starting_url in starting_urls:
        # get table view link
        starting_url_response = get_link_response(link=starting_url)

        starting_url_soup = get_soup(starting_url_response)
        table_view_url = get_link_for_table_view(soup=starting_url_soup)

        # get content from starting url when accessed in table view
        table_view_response = get_link_response(link=table_view_url)
        table_view_soup = get_soup(table_view_response)
        all_collections_on_page_details = get_collection_info(
            soup=table_view_soup,
            collections_base_link_identifier=collections_base_link_identifier,
        )
        all_page_collections = get_page_collections(all_collections_on_page_details)
        all_collections.extend(all_page_collections)

        # repeat the same logic while there is a next page
        next_page = generate_next_page_url(
            table_view_soup, next_page_link_identifier=next_page_link_identifier
        )

        for page in next_page:
            page_response = get_link_response(link=page)
            page_soup = get_soup(response=page_response)
            all_collections_on_page_details = get_collection_info(
                soup=page_soup,
                collections_base_link_identifier=collections_base_link_identifier,
            )
            all_page_collections = get_page_collections(all_collections_on_page_details)
            all_collections.extend(all_page_collections)

    for collection in all_collections:
        year_response = get_link_response(collection.details_link)
        year_soup = get_soup(year_response)
        year = get_collection_year(year_soup)
        if year:
            collection.update_collection_year(year=year)
        time.sleep(1)

    sorted_collections = sorted(all_collections, key=lambda x: (x.year, x.author))

    for collection in sorted_collections:
        download_collection_pdf(
            pdf_link=collection.pdf_link,
            pdf_name=collection.downloaded_file_name,
            fn_get_response=get_link_response,
            destination_folder="downloaded_files",
        )
        time.sleep(3)

    return all_collections


if __name__ == "__main__":
    main()
