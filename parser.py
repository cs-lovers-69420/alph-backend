# Contains functions for parsing research papers and returning information about
# the papers, such as title, authors, and citations to other papers.

def parse_html(filepath):
    title = "temp"  # Title of paper
    authors = []  # Authors of paper
    citations = []  # Titles of cited works

    ret = {"title": title, "authors": authors, "citations": citations}
    return ret
