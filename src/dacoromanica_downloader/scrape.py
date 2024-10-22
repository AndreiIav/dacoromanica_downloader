from collections import namedtuple

import requests
from bs4 import BeautifulSoup


def get_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")

    return soup


def get_next_page_url(soup: BeautifulSoup) -> str | None:
    for link in soup.find_all("a"):
        if "func=results-next-page&result_format=001" in str(link.get("href")):
            # two "next_page" links exists on the page; we need only one
            # so return as soon as one is found
            link_string = str(link.get("href"))
            next_page_url = link_string

            return next_page_url

    return None


def get_collection_info(
    soup: BeautifulSoup,
):
    CollectionInfo = namedtuple(
        "CollectionInfo", ["details_link", "title", "author", "pdf_link"]
    )
    for link in soup.find_all("a"):
        if "base=GEN01" in str(link.get("href")):
            details_link = link.get("href")
            parent = link.parent.parent
            alltd = parent.find_all("td")
            title = alltd[2].string
            if alltd[3].string:
                author = alltd[3].string
            else:
                author = ""
            pdf_link = alltd[6].find("a").get("href")

            yield CollectionInfo(
                details_link=details_link, title=title, author=author, pdf_link=pdf_link
            )


def get_collection_year(link: str) -> str | None:
    r = requests.get(link)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")
    alltd = soup.find_all("td")
    for td in alltd:
        if td.string == "Data apariţiei":
            parent = td.parent
            parent_alltd = parent.find_all("td")
            collection_year = parent_alltd[1].string

            return collection_year

    return None


def get_link_for_table_view(link: str) -> str | None:
    r = requests.get(link)
    soup = BeautifulSoup(r.content.decode("utf-8"), "html5lib")
    for _link in soup.find_all("a"):
        if "Tabel" in str(_link.string):
            table_view_link = _link.get("href")

            return table_view_link

    return None
