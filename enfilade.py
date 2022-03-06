# This file contains a description for the Enfilade class, a class used to represent
# documents in Project Alph. An Enfilade is similar to a B-tree but contains keys
# per node that represent sections of the document that are represented by any
# children of the node.

# TODO:
# 1) Is the overall substructure necessary? Do we need to make "subsections"?
# 2) If so, what about for connections that don't correspond to a subsection?

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
        When stored in memory, the filepath will include name.
        """
        self.name = name
        self.source_file = source_file  # TODO: Put the parsing stuff here maybe?

    def create_structure(self):
        """
        Creates the Enfilade structure (TODO: do this)
        """
        pass
