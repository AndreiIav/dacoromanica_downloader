import requests
from bs4 import BeautifulSoup


def get_collection_year(link: str) -> str:
    r = requests.get(link)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")
    alltd = soup.find_all("td")
    for td in alltd:
        if td.string == "Data apariţiei":
            parent = td.parent
            parent_alltd = parent.find_all("td")
            return parent_alltd[1].string
