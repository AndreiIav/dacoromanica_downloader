import time

from dacoromanica_downloader.download_pdf import download_pdf_file
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

for starting_url in starting_urls:
    url = get_link_for_table_view(link=starting_url)
    all_collections = []

    while url:
        print(url)
        soup = get_soup(url=url)
        all_collections_on_page_details = get_collection_info(soup)
        for collection_details in all_collections_on_page_details:
            new_collection = CollectionPdf(
                details_link=collection_details.details_link,
                title=collection_details.title,
                pdf_link=collection_details.pdf_link,
                author=collection_details.author,
            )

            all_collections.append(new_collection)

        url = get_next_page_url(soup=soup)
        if url is None:
            break
        time.sleep(1)

    print(f"All collections length is: {len(all_collections)}")

    for collection in all_collections:
        collection.update_collection_year(fn_get_collection_year=get_collection_year)
        time.sleep(1)

    sorted_collections = sorted(all_collections, key=lambda x: (x.year, x.author))

    for collection in sorted_collections:
        download_pdf_file(
            pdf_link=collection.pdf_link,
            pdf_name=collection.downloaded_file_name,
            destination_folder="downloaded_files",
        )
        time.sleep(3)
