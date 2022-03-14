# Test scripts for Project Alph backend work
# TODO: switch to Unittest

import sys
from docgraph import DocGraph


def test_docgraph():
    test_graph = DocGraph()

    # Test adding nodes
    print("Testing adding nodes")
    nodes = ["node1", "node2", "node3"]
    for node in nodes:
        test_graph.add_node(node)
    added_nodes = test_graph.get_nodes()
    for node in nodes:
        assert(node in added_nodes)

    # Simple edges
    print("Testing edges")
    test_graph.add_edge("node1", "node2")
    test_graph.add_edge("node1", "node3")
    assert("node2" in test_graph.get_edges("node1"))
    assert("node3" in test_graph.get_edges("node1"))
    assert("node1" in test_graph.get_edges("node3"))
    assert("node1" in test_graph.get_edges("node2"))
    assert("node1" not in test_graph.get_edges("node1"))
    assert("node2" not in test_graph.get_edges("node2"))
    assert("node3" not in test_graph.get_edges("node3"))
    assert("node2" not in test_graph.get_edges("node3"))
    assert("node3" not in test_graph.get_edges("node2"))

    # Test reset
    print("Testing reset")
    test_graph.reset()
    assert(test_graph.get_nodes() == [])
    assert(test_graph.elements == {})


if __name__ == '__main__':
    if "-d" in sys.argv:
        test_docgraph()
