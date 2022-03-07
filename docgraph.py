# This file contains methods for the document graph used in Project Alph. The
# document graph contains nodes for each document, where each node is an
# Enfilade specified in enfilade.py (NOTE: at the moment, an Enfilade just
# contains a filename). Each node has connections to other documents to
# represent citations or links between documents. Each citation contains
# information on where in the cited document the citation appears. To determine
# citations, the Node class runs the parser.

import parser
from enfilade import Enfilade


class Node:

    def __init__(self, source_file):
        self.source_file = source_file
        self.connections = []  # List of connections to other documents

        # Parse provided file and get information about document
        paper_info = parser.parse_html(source_file)
        self.title = paper_info["title"]
        self.authors = paper_info["authors"]
        self.citations = paper_info["citations"]

        # Store document as an Enfilade
        self.document = Enfilade(self.title, self.source_file)


class DocGraph:

    def __init__(self):
        # An adjacency list representation of a graph indexed by title
        self.elements = {}
        # A list of documents not in the graph but that the user might want
        self.suggested_docs = []

    def add_node(self, filepath):
        """Add a new node to the graph"""
        new_node = Node(filepath)
        self.elements[new_node.title] = {"Node": new_node, "Edges": []}

        # If this new node was one of the suggested ones, remove it from there
        if new_node.title in self.suggested_docs:
            self.suggested_docs.remove(new_node.title)

    def add_edge(self, node1, node2):
        """
        Adds an edge between two nodes in the graph. Returns T/F based on success.
        Takes two strings as input.
        """
        # Verify that both are in the graph
        if node1 not in self.elements or node2 not in self.elements:
            print("Error: node not found")
            return False

        # Check if the edge already exists
        if node2 in self.elements[node1]["Edges"] or \
                node1 in self.elements[node2]["Edges"]:
            return True

        self.elements[node1]["Edges"].append(node2)
        self.elements[node2]["Edges"].append(node1)

    def add_all_connections(self, node_name, suggest=True):
        """
        Adds all the connections for a specified node. Takes one string as input.
        If suggest is True, then for any citation that isn't found in the graph,
        add it to the suggested_docs list. Otherwise, only make connections to nodes
        already in the graph.
        """
        if node_name not in self.elements:
            print("Error: node not found")
            return False

        node = self.elements[node_name]["Node"]
        # Make a connection for every citation
        for ref in node.citations:
            if ref in self.elements:
                self.add_edge(node_name, ref)
            elif suggest and ref not in self.suggested_docs:
                self.suggested_docs.append(ref)


if __name__ == '__main__':
    documents = DocGraph()

    documents.add_node("path/to/file1")
    documents.add_node("path/to/file2")
    documents.add_edge("file1", "file2")
    print(documents.elements)
    print(documents.suggested_docs)
    documents.add_all_connections("file1")
    print(documents.elements)
    print(documents.suggested_docs)
    documents.add_node("path/to/doc2")
    print(documents.elements)
    documents.add_all_connections("file1")
    print(documents.elements)
    print(documents.suggested_docs)
