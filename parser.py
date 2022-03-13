# Contains functions for parsing research papers and returning information about
# the papers, such as title, authors, and citations to other papers.

from collections import defaultdict
import os
import urllib3
from bs4 import BeautifulSoup


def parse_html(filepath):
    title = os.path.basename(filepath)  # Title of paper (FIXME)
    authors = []  # Authors of paper
    citations = ["doc1", "doc2", "doc3"]  # Titles of cited works

    if not os.path.exists(filepath):
        print("Path doesn't exist")
        return
    file = open(filepath)
    soup = BeautifulSoup(file, 'html.parser')
    print(soup.title)

    for link in soup.find_all('a'):
        print(link.get('href'))  # TODO: Need to filter these links

    ret = defaultdict(None)
    ret["title"] = title
    ret["authors"] = authors
    ret["citations"] = citations

    return ret


if __name__ == '__main__':
    parse_html(
        "Tests/The Covid-19 Pandemic Has Lasted 2 Years. The Next Steps Are Divisive. - The New York Times.html")
