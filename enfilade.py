# This file contains a description for the Enfilade class, a class used to represent
# documents in Project Alph. An Enfilade is similar to a B-tree but contains keys
# per node that represent sections of the document that are represented by any
# children of the node.

# TODO:
# 1) Need some sort of info about where in the document citations are made. Might
#    need to move the edge logic into here.

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
        self.source_file = source_file  # TODO: Put the parsing stuff here maybe?

    def create_structure(self):
        """
        Creates the Enfilade structure (TODO: do this)
        """
        pass
