import time

from download_pdf import download_pdf_file
from get_collection_info import get_collection_info
from get_collection_year import get_collection_year
from get_next_page import get_next_page_url
from get_soup import get_soup
from model import CollectionPdf
from switch_start_page_view import get_link_for_table_view

starting_url = "http://digitool.bibmet.ro:8881/R/NN8U4KJ5666B5P2925X5FFMKP3CYP8KYUQNJ7DX882UTVPGFG3-05921?func=collections-result&collection_id=1719"
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
