# This file contains a description for the Enfilade class, a class used to represent
# documents in Project Alph. An Enfilade is similar to a B-tree but contains keys
# per node that represent sections of the document that are represented by any
# children of the node.

# TODO:
# 1) Need some sort of info about where in the document citations are made. Might
#    need to move the edge logic into here.

from collections import defaultdict


class Enfilade:
    """
    An Enfilade class designed for Project Alph. Can make subtrees at the paragraph level.
    Similar to a B-tree but employs dsps and wids to faciliate easy lookup and moving.
    """

    # NOTE: This implementation below is not an Enfilade. If it will be useful in the future,
    # the implementation will then be finished.

    def __init__(self, name, source_file):
        """
        Creates an Enfilade with specified name from a preprocessed source file.
        When stored in memory, the filepath will be a textfile [source_file].enf.
        """
        self.name = name
        self.source_file = source_file
        self.references = defaultdict(lambda: [])
        self.text = ""

    def create_structure(self):
        """
        Creates the Enfilade structure (TODO: do this)
        """
        pass

    def add_citations(self, citation_list):
        """
        Reads in a list of citations for the document (provided by the parser)
        and stores them as data for the Enfilade. citation_list is a list of
        tuples (title, [page_numbers]) for every citation in the document.
        """
        # This will be a dictionary keyed by title, where the value is a list of
        # page numbers where that title is cited.
        citation_list = list(dict.fromkeys(citation_list))
        for pair in citation_list:
            self.references[pair[0]].append(pair[1])

    def add_text(self, text):
        """
        Stores text of associated file
        """
        self.text = text

    def get_citations(self):
        """
        Return a list of cited documents (not including the page numbers).
        """
        refs = [title for title in self.references]
        return refs

    def get_text(self):
        """Returns text of document"""
        return self.text

    def get_cited_pages(self, title):
        """
        Gets the page numbers where 'title' is cited
        """
        for ref in self.references:
            if title in ref:
                return self.references[ref]
        print("Error: not found")
        return [-1]
