import requests
from bs4 import BeautifulSoup


def get_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")

    return soup
