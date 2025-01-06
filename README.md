# Overview
This is a Python package to automatically download PDF files from [Biblioteca Digitala a Bucureștilor website](http://digitool.bibmet.ro:8881/R/PSCBLKPMY6HF14YIT63KQK1UNMBQV4VKUJY67SPN152CK7AI3F-01191?func=search). 

# Features
- automatically downloads PDF files
- names the PDF file according to this rule: 'author'\_'title'\_'year'.pdf. Only the 'title' is mandatory, the 'author' and 'year' will not be added to the name if they are not found
- names longer than 250 characters (including file system path) are shortened to 250 characters length (to comply with Windows file length limitation). If the name cannot be properly shortened, the PDF file will not be downloaded


# Installation
Pull down the source code from GitHub:\
`git clone https://github.com/AndreiIav/dacoromanica_downloader.git`

Change the current working directory to 'dacoromanica_downloader' folder.

Create and activate a virtual environment:\
On Linux:\
Create the virtual environment:\
`python3 -m venv venv`\
Activate the virtual environment:\
`source venv/bin/activate`

On Windows:\
Create the virtual environment:\
`python -m venv venv`\
Activate the virtual environment:\
`venv\Scripts\activate`

Install the python packages specified in requirements.txt:\
`(venv) $ pip install -r requirements.txt`

Install the dacoromanica_downloader package:\
`(venv) $ pip install -e .`

# Collections page
**dacoromanica_downloader** works by crawling collections pages and extracting data from them. A collections page is one that consists of multiple PDF file links and their details. An example of a collections page is: \
http://digitool.bibmet.ro:8881/R/6SV4A783G2FGNA2Q3UDUIS2YD1HNIGQLHGEGSV5G55V6VDU53M-04211?func=collections-result&collection_id=1413 .\
Another example can be found in the _starting_urs.txt_ file. **dacoromanica_downloader** will not work if any other type of _Biblioteca Digitala a Bucureștilor_ url is used.

# Downloading PDF files
Add the desired collections page link to the **starting_urls.txt** file. If  there are multiple pages for the collection (like in the example from the previous section), only the first page url needs to be added. The next pages will be crawled automatically. The default link present in the **starting_urls.txt** file is a valid one, but is there only as an example and can be deleted. Multiple collections page links can be added one after another (separated by a space) or on separate lines.

Run dacoromanica_downloader:\
`(venv) $ python -m dacoromanica_downloader.main`

The PDF files will be downloaded in the **downloaded_files** folder.

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