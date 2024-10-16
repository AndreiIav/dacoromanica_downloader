import requests
from bs4 import BeautifulSoup


def get_link_for_table_view(link: str) -> str:
    r = requests.get(link)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")
    for link in soup.find_all("a"):
        if "Tabel" in str(link.string):
            return link.get("href")
