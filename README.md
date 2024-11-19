# Overview
This is a Python package to automatically download PDF files from [Dacoromanica website](http://digitool.bibmet.ro:8881/R/PSCBLKPMY6HF14YIT63KQK1UNMBQV4VKUJY67SPN152CK7AI3F-01191?func=search). 


# Installation
Pull down the source code from GitHub:\
`git clone https://github.com/AndreiIav/dacoromanica_downloader.git`

Change directory to dacoromanica_downloader folder.

Create a new virtual environment

Activate the virtual environment

Install the python packages specified in requirements.txt:\
`(venv) $ pip install -r requirements.txt`

Install the dacoromanica_downloader package:\
`pip install -e .`

# Dacoromanica collections page
dacoromanica_downloader works by crawling collection pages and extracting data from them. A Dacoromanica collections page is one that consists of multiple PDF file links and its details. An example of a Dacoromanica collections page is: \
http://digitool.bibmet.ro:8881/R/6SV4A783G2FGNA2Q3UDUIS2YD1HNIGQLHGEGSV5G55V6VDU53M-04211?func=collections-result&collection_id=1413 .\
Another example can be found in the **starting_urs.txt** file. dacoromanica_downloader will not work if any other type of Dacoromanica webpage url is used.

# Downloading PDF files
Add the desired Dacoromanica collection page link to the **starting_urs.txt** file. The default link present there is only for demonstration purposes and can be deleted. Multiple links can be added one after another (separated by a space) or on separate lines.

Run dacoromanica_downloader:\
`(venv) python -m dacoromanica_downloader.main`

The PDF files will be downloaded in the **downloaded_files** folder.

# Features
- downloads Dacoromanica PDF files
- names the pdf file according to this rule: 'author'\_'title'\_'year'.pdf. Only the 'title' is mandatory, the 'author' and 'year' will not be added to the name if they are not found
- names longer than 250 characters (including file system path) are shortened to 250 characters length (to comply with Windows file length limitation). If the name cannot be properly shortened, the PDF file will not be downloaded

# Key Python Modules Used
- **requests**: Python library for HTTP requests
- **beautifulsoup4**: Python library for pulling data out of HTML and XML files
- **pytest**: framework for testing Python projects
- **pytest-cov**: pytest extension for running coverage\.py to check code coverage of tests
- **mypy**: static type checker for Python

This application was written using Python 3.10.


# Testing
To run all the tests:\
`(venv) $ pytest`

To check the code coverage of the tests:\
`(venv) $ pytest --cov-report term-missing --cov=src`




