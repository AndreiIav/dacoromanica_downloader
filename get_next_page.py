def get_next_page_url(soup):
    for link in soup.find_all("a"):
        if "func=results-next-page&result_format=001" in str(link.get("href")):
            # two "next_page" links exists on the page; we need only one
            # so return as soon as one is found
            link_string = str(link.get("href"))
            next_page_url = link_string
            return next_page_url
