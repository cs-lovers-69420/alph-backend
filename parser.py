# Contains functions for parsing research papers and returning information about
# the papers, such as title, authors, and citations to other papers.

from collections import defaultdict
import os


def parse_html(filepath):
    title = os.path.basename(filepath)  # Title of paper (FIXME)
    authors = []  # Authors of paper
    citations = ["doc1", "doc2", "doc3"]  # Titles of cited works

    ret = defaultdict(None)
    ret["title"] = title
    ret["authors"] = authors
    ret["citations"] = citations

    return ret
