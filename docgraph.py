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

    def __init__(self, source_file, main=False):
        self.source_file = source_file

        # Parse provided file and get information about document
        paper_info = parser.parse(source_file)
        self.title = paper_info["title"]
        self.authors = paper_info["authors"]
        self.main = main  # Whether or not this is a "main" document

        # Store document as an Enfilade
        self.document = Enfilade(self.title, self.source_file)

        # Set citations
        self.set_citations(paper_info["citations"])

    def set_citations(self, citation_list):
        """
        Sets the citations for this node to the provided list.
        """
        self.document.add_citations(citation_list)

    def get_citations(self):
        """
        Returns a list of the citations for this node.
        """
        return self.document.get_citations()

    def get_info(self):
        """Returns a dictionary containing info about this node"""
        data = {"title": self.title, "source": self.source_file}
        return data


class DocGraph:

    def __init__(self):
        # An adjacency list representation of a graph indexed by title
        self.elements = {}
        # A list of documents not in the graph but that the user might want
        self.suggested_docs = []

    def add_node(self, filepath, main=False):
        """Add a new node to the graph"""
        new_node = Node(filepath, main)
        if new_node.title in self.elements:
            # Instead of raising an error, just silently exit
            # TODO: Raise a warning instead?
            return
        self.elements[new_node.title] = {"Node": new_node, "Edges": []}

        # If this new node was one of the suggested ones, remove it from there
        # TODO: automatically add the relevant citation?
        for citation in self.suggested_docs:
            if new_node.title in citation:
                self.suggested_docs.remove(citation)
                break

        # if new_node.title in self.suggested_docs:
        #     self.suggested_docs.remove(new_node.title)

    def add_edge(self, node1, node2):
        """
        Adds an edge between two nodes in the graph. Returns T/F based on success.
        Takes two strings as input.
        """
        # Verify that both are in the graph
        if node1 not in self.elements:
            raise KeyError(f"'{node1}' could not be found")
        elif node2 not in self.elements:
            raise KeyError(f"'{node2}' could not be found")

        # Check if the edge already exists
        if node2 in self.elements[node1]["Edges"] or \
                node1 in self.elements[node2]["Edges"]:
            return True

        # Create the edge
        self.elements[node1]["Edges"].append(node2)
        self.elements[node2]["Edges"].append(node1)
        return True

    def add_all_connections(self, node_name, suggest=True):
        """
        Adds all the connections for a specified node. Takes one string as input.
        If suggest is True, then for any citation that isn't found in the graph,
        add it to the suggested_docs list. Otherwise, only make connections to nodes
        already in the graph.
        """
        if node_name not in self.elements:
            # TODO: Raise an error
            raise KeyError(f"'{node_name}' could not be found")

        node = self.elements[node_name]["Node"]
        # Make a connection for every citation
        for citation in node.get_citations():
            found = False
            for title in self.elements:
                if title in citation:
                    self.add_edge(node_name, title)
                    found = True
                    break
            if suggest and not found:
                self.suggested_docs.append(citation)

    def make_all_graph_connections(self):
        """
        Make connections for all nodes in the graph
        """
        for node_name in self.elements:
            node = self.elements[node_name]["Node"]
            if node.main:
                self.add_all_connections(node_name, suggest=True)
            else:
                self.add_all_connections(node_name, suggest=False)

    def list_nodes(self):
        """Return a list of all nodes in the graph."""
        return [node for node in self.elements]

    def get_node(self, req_node) -> Node:
        """Return the requested node object."""
        if req_node in self.elements:
            return self.elements[req_node]["Node"]
        else:
            raise KeyError(f"'{req_node}' could not be found")

    def list_edges(self, req_node):
        """Return a list of all edges for a specified node."""
        if req_node in self.elements:
            return [node for node in self.elements[req_node]["Edges"]]
        else:
            raise KeyError(f"'{req_node}' could not be found")

    def get_graph(self):
        """Returns the dictionary representation of the graph."""
        return self.elements

    def reset(self):
        """
        Reset the docgraph. Used for testing purposes.
        """
        self.elements = {}
        self.suggested_docs = []


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
