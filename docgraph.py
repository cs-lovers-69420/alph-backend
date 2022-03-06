# This file contains code for the document graph used in Project Alph. The
# document graph contains nodes for each document, where each node is an
# Enfilade specified in enfilade.py (NOTE: at the moment, an Enfilade just
# contains a filename). Each node has connections to other documents to
# represent citations or links between documents. Each citation contains
# information on where in the cited document the citation appears. To determine
# citations, the Node class runs the parser.

import parser


class Node:

    def __init__(self, source_file):
        self.source_file = source_file

        # Parse provided file and get information about
        paper_info = parser.parse_html(source_file)
        self.title = paper_info["title"]
        self.authors = paper_info["authors"]
        self.citations = paper_info["citations"]


if __name__ == '__main__':
    test = Node("hello there")
    print(test.title, test.authors, test.citations)
