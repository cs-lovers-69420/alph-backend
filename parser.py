# Contains functions for parsing research papers and returning information about
# the papers, such as title, authors, and citations to other papers.

from collections import defaultdict
import os
import re
import requests
from bs4 import BeautifulSoup


def _parse_html(filepath):
    """
    Gets information from an html file (TODO: add hyperlink functionality?)
    NOTE: Might need to modify for paper links, but vast majority of functionality probably
    going to be PDFs.
    """
    title = ""  # Title of paper (FIXME)
    authors = []  # Authors of paper (TODO: get by regex search maybe?)
    citations = []  # Titles of cited works

    # Get file
    if not os.path.exists(filepath):
        print("Path doesn't exist")
        return
    html = open(filepath)
    soup = BeautifulSoup(html, 'html.parser')

    # Get title from HTML title (NOTE: might not work?)
    title = soup.title.string

    # Get all links and titles of webpages they correspond to
    # TODO: If adding hyperlink functionality, might want to return links instead of titles
    all_links = [tag['href'] for tag in soup.select('p a[href]')]
    for link in all_links:
        response = requests.get(link)
        citations.append(BeautifulSoup(
            response.text, "html.parser").title.string)

    print(citations)

    ret = defaultdict(lambda: None)
    ret["title"] = title
    ret["authors"] = authors
    ret["citations"] = citations

    return ret


def _parse_pdf(filepath):
    ret = defaultdict(lambda: None)
    ret["title"] = os.path.basename(filepath)
    ret["authors"] = []
    ret["citations"] = []
    return ret


def _parse_test(filepath):
    """
    "Dummy" parser used in the test script.
    """
    ret = defaultdict(lambda: None)
    ret["title"] = os.path.basename(filepath)
    ret["authors"] = []
    ret["citations"] = []
    return ret


def parse(filepath):
    """
    Function called externally to parse a file. Calls either the html or pdf parser
    depending on filepath.
    """
    # Verify that path exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"'{filepath}' does not exist")

    if filepath.endswith(".html"):
        return _parse_html(filepath)
    elif filepath.endswith(".pdf"):
        return _parse_pdf(filepath)
    else:
        return _parse_test(filepath)


# if __name__ == '__main__':
#     parse(
#         "Tests/The Covid-19 Pandemic Has Lasted 2 Years. The Next Steps Are Divisive. - The New York Times.html")
