from collections import namedtuple
from typing import Callable, Optional

import requests
from bs4 import BeautifulSoup

from dacoromanica_downloader.download_pdf import get_link_response


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


def get_collection_info(soup: BeautifulSoup, collections_base_link_identifier: str):
    """
    Yields information about each item in a collection from parsed HTML content.

    This generator function extracts specific details for each item in a
    collection represented in the HTML content of a BeautifulSoup object. For
    each item, it yields a named tuple containing the item's link, title,
    author, and a link to its PDF file.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed
        HTML content.
        collections_base_link_identifier (str): The name used to identify the HTML unit that
        contains a collection.

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


def get_link_for_table_view(
    link: str,
    fn_get_response: Callable[
        [str, Optional[Callable]], requests.Response | str
    ] = get_link_response,
) -> str | None:
    """
    Retrieves the URL for the table view from an URL.

    This function fetches HTML content from the provided URL and searches for
    the table view URL. It returns the link as a string, or, if an HTTP
    exception occurs or the link is not found, None. A custom function can be
    provided to handle the HTTP request, defaulting to 'get_link_response'.

    Args:
        link (str): The URL of the page from which to retrieve the table view
        link.
        fn_get_response (Callable): A function to fetch the HTTP response for
        the URL. Defaults to 'get_link_response'.

    Returns:
        str | None: The URL for the table view as a string if found, or None if
        it was not found or an HTTP exception occurred.
    """
    response = fn_get_response(link)
    if not isinstance(response, requests.Response):
        return None

    soup = BeautifulSoup(response.content.decode("utf-8"), "html5lib")
    for _link in soup.find_all("a"):
        if "Tabel" in str(_link.string):
            table_view_link = _link.get("href")

            return table_view_link

    return None
