from collections import namedtuple
from typing import Iterator

import requests
from bs4 import BeautifulSoup


def get_soup(response: requests.Response) -> BeautifulSoup:
    """
    Parses the content of an HTTP response into a BeautifulSoup object.

    This function takes an HTTP response object and parses its content as HTML
    using BeautifulSoup.

    Args:
        response (requests.Response): The HTTP response object containing the
        content to be parsed.

    Returns:
        BeautifulSoup : A BeautifulSoup object representing the parsed HTML
        content.
    """

    soup = BeautifulSoup(response.content.decode("utf-8"), "html5lib")

    return soup


def get_next_page_url(
    soup: BeautifulSoup,
    next_page_link_identifier: str,
) -> str | None:
    """
    Extracts URL from a BeautifulSoup object, if available.

    This function searches the parsed HTML content (BeautifulSoup object) for
    a link to the next page. If a "next page" URL is found, it returns the URL
    as a string; otherwise, it returns None.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed
        HTML content.
        next_page_link_identifier (str): The name used to identify the searched
        link.

    Returns:
        str | None: The URL of the next page as a string if found, otherwise
        None.
    """
    for link in soup.find_all("a"):
        if next_page_link_identifier in str(link.get("href")):
            # two "next_page" links exists on the page; we need only one
            # so return as soon as one is found
            next_page_url = str(link.get("href"))

            return next_page_url

    return None


def get_collection_info(
    soup: BeautifulSoup, collections_base_link_identifier: str
) -> Iterator:
    """
    Yields information about each item in a collection from parsed HTML content.

    This generator function extracts specific details for each item in a
    collection represented in the HTML content of a BeautifulSoup object. For
    each item, it yields a named tuple containing the item's link, title,
    author, and a link to its PDF file.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed
        HTML content.
        collections_base_link_identifier (str): The name used to identify the
        HTML unit that contains a collection.

    Yields:
        CollectionInfo (namedtuple): A named tuple with the following
        attributes: 'details_link', 'title', 'author', and 'pdf_link'.
    """
    CollectionInfo = namedtuple(
        "CollectionInfo", ["details_link", "title", "author", "pdf_link"]
    )
    for link in soup.find_all("a"):
        if collections_base_link_identifier in str(link.get("href")):
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


def get_collection_year(soup: BeautifulSoup) -> str | None:
    """
    Extracts the publication year of a collection from a BeautifulSoup object.

    This function searches the parsed HTML content (BeautifulSoup object) for a
    publication year. If the year is found, it is returned as a string. If no
    year is found, the function returns None.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed
        HTML content of the collection page.

    Returns:
        str | None: The publication year as a string if found, otherwise None.
    """

    alltd = soup.find_all("td")
    for td in alltd:
        if td.string == "Data apariţiei":
            parent = td.parent
            parent_alltd = parent.find_all("td")
            collection_year = parent_alltd[1].string

            return collection_year

    return None


def get_link_for_table_view(soup: BeautifulSoup) -> str | None:
    """
    Extracts the URL for the table view from a BeautifulSoup object.

    This function searches the parsed HTML content (BeautifulSoup object) for a
    table view link. If the link is found, it is returned as a string, if not
    the function returns None.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed
        HTML content of the collection page.

    Returns:
        str | None: The URL for the table view as a string if found, otherwise
        None.
    """

    for link in soup.find_all("a"):
        if "Tabel" in str(link.string):
            table_view_link = link.get("href")

            return table_view_link

    return None
