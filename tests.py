# Test scripts for Project Alph backend work
# TODO: switch to Unittest

from cgi import test
from re import T
import sys
import os
from docgraph import DocGraph


def test_docgraph():
    """
    Tests for the graph
    """
    test_graph = DocGraph()

    # Test adding nodes
    print("Test adding nodes")
    nodes = ["TestData/node1", "TestData/node2", "TestData/node3"]
    for node in nodes:
        test_graph.add_node(node)
    added_nodes = test_graph.list_nodes()
    for node in nodes:
        assert(os.path.basename(node) in added_nodes)

    # Simple edges
    print("Test edges")
    test_graph.add_edge("node1", "node2")
    test_graph.add_edge("node1", "node3")
    assert("node2" in test_graph.list_edges("node1"))
    assert("node3" in test_graph.list_edges("node1"))
    assert("node1" in test_graph.list_edges("node3"))
    assert("node1" in test_graph.list_edges("node2"))
    assert("node1" not in test_graph.list_edges("node1"))
    assert("node2" not in test_graph.list_edges("node2"))
    assert("node3" not in test_graph.list_edges("node3"))
    assert("node2" not in test_graph.list_edges("node3"))
    assert("node3" not in test_graph.list_edges("node2"))

    # Test reset
    print("Test reset")
    test_graph.reset()
    assert(test_graph.list_nodes() == [])
    assert(test_graph.elements == {})

    # Already existing node
    print("Test adding node that already exists")
    test_graph.add_node("TestData/node1")
    test_graph.add_node("TestData/node1")
    assert(len(test_graph.list_nodes()) == 1)

    # Already existing edge
    print("Test adding edge that already exists")
    test_graph.add_node("TestData/node2")
    test_graph.add_edge("node1", "node2")
    test_graph.add_edge("node2", "node1")
    assert(len(test_graph.list_edges("node1")) == 1)
    assert(len(test_graph.list_edges("node2")) == 1)

    # Edge to nonexistent node
    # TODO: make this more elegant for handling raised errors
    print("Test adding edge to nonexistent node")
    try:
        test_graph.add_edge("node1", "node3")
        assert(False)
    except KeyError:
        assert(True)
    try:
        test_graph.add_edge("node3", "node1")
        assert(False)
    except KeyError:
        assert(True)
    try:
        test_graph.add_edge("node3", "node4")
        assert(False)
    except KeyError:
        assert(True)

    # Test nonexistent file
    print("Test nonexistent file")
    try:
        test_graph.add_node("TestData/nonexistent")
        assert(False)
    except FileNotFoundError:
        assert(True)

    # Test adding all connections
    print("Test adding all connections")
    test_graph.reset()
    test_graph.add_node("TestData/node1")
    test_graph.add_node("TestData/node2")
    test_graph.add_node("TestData/node3")
    test_graph.add_node("TestData/node4")
    # Manually set citations for node1
    node = test_graph.get_node("node1")
    cits = [("node2", 0), ("node3", 2), ("node4", 1), ("node5", 2)]
    node.set_citations(cits)
    test_graph.add_all_connections("node1")
    connections = test_graph.list_edges("node1")
    assert("node2" in connections)
    assert("node3" in connections)
    assert("node4" in connections)
    assert("node5" in test_graph.suggested_docs)

    # Test if suggested docs is updated properly
    print("Test removal from document suggestions")
    test_graph.add_node("TestData/node5")
    assert("node5" not in test_graph.suggested_docs)


def test_parser():
    """
    Tests for the parser
    """


def test_general():
    """
    General tests that involve both graph and parser
    """
    test_graph = DocGraph()

    # Test automatic addition of citations
    print("Test automatic addition of citations")
    test_graph.reset()
    test_graph.add_node("TestData/sciadv.abj2479.pdf")
    test_graph.add_node(
        "TestData/Rasmussen2011_Article_AnOpenSystemFrameworkForIntegr.pdf")
    nodes = test_graph.list_nodes()
    test_graph.add_all_connections(nodes[0])
    assert(nodes[1] in test_graph.list_edges(nodes[0]))


if __name__ == '__main__':
    if "-d" in sys.argv:
        test_docgraph()
    if "-p" in sys.argv:
        test_parser()
    if "-g" in sys.argv:
        test_general()
