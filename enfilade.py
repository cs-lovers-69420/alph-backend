# This file contains a description for the Enfilade class, a class used to represent
# documents in Project Alph. An Enfilade is similar to a B-tree but contains keys
# per node that represent sections of the document that are represented by
# any children of the node.

# TODO:
# 1) Is the overall substructure necessary? Do we need to make "subsections"?
# 2) If so, what about for connections that don't correspond to a subsection?
