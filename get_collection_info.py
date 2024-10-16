def get_collection_info(soup):
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

            yield details_link, title, author, pdf_link
