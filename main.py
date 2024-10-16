import time

from download_pdf import download_pdf_file
from get_starting_urls import get_starting_urls
from model import CollectionPdf
from scrape import (
    get_collection_info,
    get_collection_year,
    get_link_for_table_view,
    get_next_page_url,
    get_soup,
)

starting_urls_file_path: str = "starting_urls.txt"
starting_urls: list = get_starting_urls(starting_urls_file_path)

for starting_url in starting_urls:
    url = get_link_for_table_view(starting_url)
    all_collections = []

    while url:
        print(url)
        soup = get_soup(url)
        all_collections_on_page_details = get_collection_info(soup)
        for collection_details in all_collections_on_page_details:
            new_collection = CollectionPdf(
                details_link=collection_details[0],
                title=collection_details[1],
                author=collection_details[2],
                pdf_link=collection_details[3],
            )
            all_collections.append(new_collection)

        url = get_next_page_url(soup)
        if url is None:
            break
        time.sleep(1)

    print(f"All collections length is: {len(all_collections)}")

    for collection in all_collections:
        collection.update_collection_year(get_collection_year)
        time.sleep(1)

    sorted_collections = sorted(all_collections, key=lambda x: (x.year, x.author))

    for collection in sorted_collections:
        download_pdf_file(
            collection.pdf_link, collection.downloaded_file_name, "downloaded_files"
        )
        time.sleep(3)
