from typing import Optional


class CollectionPdf:
    def __init__(
        self,
        details_link: str,
        title: str,
        author: Optional[str] = "",
        year: Optional[int] = 0,
        pdf_link: Optional[str] = None,
    ):
        self.details_link = details_link
        self.title = title
        self.author = author
        self.year = year
        self.pdf_link = pdf_link

    def __repr__(self) -> str:
        return f"CollectionPdf({self.details_link},{self.title},{self.year})"

    def __str__(self) -> str:
        return f"title: {self.title}, author: {self.author}, year: {self.year}"

    def __gt__(self, other) -> bool:
        if self.year is None:
            return False
        if other.year is None:
            return True
        return self.year > other.year

    def update_collection_year(self, fn_get_collection_year) -> None:
        link = self.details_link
        year = fn_get_collection_year(link)
        if year:
            self.year = self._format_year(year)

    @property
    def downloaded_file_name(self):
        title = self._remove_forbidden_charactes(self.title)
        author = self._remove_forbidden_charactes(self.author)

        if self.year and author:
            return f"{author}_{title}_{self.year}.pdf"
        elif self.year:
            return f"{title}_{self.year}.pdf"
        elif author:
            return f"{author}_{title}.pdf"
        else:
            return f"{title}.pdf"

    def _remove_forbidden_charactes(self, name: str) -> str:
        """
        Remove characters that cannot be a part of file names on Linux
        or Windows: <>:'""/'\\|/?*
        It uses Unicode code points of the forbidden charactes.
        """
        res = ""
        for character in name:
            if ord(character) not in (60, 62, 58, 39, 47, 39, 92, 124, 47, 63, 42):
                res += character

        return res

    def _format_year(self, yr: str) -> int:
        year = ""
        for x in yr:
            if x.isdigit():
                year += x

        try:
            res = int(year[:4])
        except ValueError:
            return 0

        return res
