# Contains functions for parsing research papers and returning information about
# the papers, such as title, authors, and citations to other papers.

from collections import defaultdict
import os
import re
import requests
from bs4 import BeautifulSoup


def parse_html(filepath):
    """
    Gets information from an html file (TODO: add hyperlink functionality?)
    NOTE: Might need to modify for paper links, but vast majority of functionality probably
    going to be PDFs.
    """
    title = ""  # Title of paper (FIXME)
    authors = []  # Authors of paper
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
    print(all_links)
    for link in all_links:
        response = requests.get(link)
        citations.append(BeautifulSoup(
            response.text, "html.parser").title.string)

    print(citations)

    ret = defaultdict(None)
    ret["title"] = title
    ret["authors"] = authors
    ret["citations"] = citations

    return ret


if __name__ == '__main__':
    parse_html(
        "Tests/The Covid-19 Pandemic Has Lasted 2 Years. The Next Steps Are Divisive. - The New York Times.html")
