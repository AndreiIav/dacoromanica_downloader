from __future__ import annotations


class CollectionPdf:
    """
    Represents metadata and details of a PDF file to be downloaded.

    The class encapsulates information about a single PDF file including the
    link to all details of the document (details_link), title, download link,
    author, and publication year.

    Attributes:
        details_link (str): The URL to the details page of the collection item.
        title (str): The title of the collection item.
        pdf_link (str): The URL to download the PDF file.
        author (str): The author of the collection item. Defaults to an empty
        string.
        year (int): The publication year of the collection item. Defaults to 0.

    Methods:
        update_collection_year: Updates the collection's year attribute with a
        formatted year.
        downloaded_file_name: Gets the name used for the downloaded collection
        file.
    """

    def __init__(
        self,
        details_link: str,
        title: str,
        pdf_link: str,
        author: str = "",
        year: int = 0,
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

    def __gt__(self, other: CollectionPdf) -> bool:
        return self.year > other.year

    def update_collection_year(
        self,
        year: str,
    ) -> None:
        """
        Updates the collection's year attribute with a formatted year.

        This method takes a year as a string, tries to format it into an integer
        using the '_format_year' method, and, if successful, updates the 'year'
        attribute of the instance.

        Args:
            year (str): The year to be formatted.

        Returns:
            None: This method does not return a value.
        """
        self.year = self._format_year(year_to_format=year)

    @property
    def downloaded_file_name(self) -> str:
        """
        Gets the name used for the downloaded collection pdf file.

        This method sanitazes the collection's title and year by removing
        characters not allowed in Windows file names. The file name is then
        constructed according to what collection details exist: author, title
        and year.
        """
        title = self._remove_forbidden_charactes(name=self.title)
        author = self._remove_forbidden_charactes(name=self.author)

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
        Removes characters from a string that are not allowed in file names on
        Windows.

        This method filters out characters that are forbidden in file names due
        to operating system restrictions. The forbidden characters are: '<',
        '>', ':', ''', '"', '/', '\\', '|', '?', '*'.
        The method uses Unicode code points to identify and remove these
        characters.

        Args:
            name (str): The string representing the file name to be sanitized.

        Returns:
            str: The sanitized file name with forbidden characters removed.
        """
        res = ""
        for character in name:
            if ord(character) not in (60, 62, 58, 39, 47, 39, 92, 124, 47, 63, 42):
                res += character

        return res

    def _format_year(self, year_to_format: str) -> int:
        """
        Formats a year string by extracting and converting digits to an integer.

        This method processes a string to extract only numeric characters. It
        then attempts to convert the digits into an integer. If the conversion
        fails, it returns 0.

        Args:
            year_to_format (str): A string containing the year information.

        Returns:
            int: The formatted year if successful, otherwise 0.
        """
        year = ""
        for character in year_to_format:
            if character.isdigit():
                year += character

        try:
            res = int(year[:4])
        except ValueError:
            return 0

        return res
