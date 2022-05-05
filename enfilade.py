# This file contains a description for the Enfilade class, a class used to represent
# documents in Project Alph. An Enfilade is similar to a B-tree but contains keys
# per node that represent sections of the document that are represented by any
# children of the node.

import os
import pathlib
from collections import defaultdict
from pdf2image import convert_from_path
import fitz

import parser


class Enfilade:
    """
    An Enfilade class designed for Project Alph. Can make subtrees at the paragraph level.
    Similar to a B-tree but employs dsps and wids to faciliate easy lookup and moving.
    """

    # NOTE: This implementation below is not an Enfilade. If it will be useful in the future,
    # the implementation will then be finished.

    def __init__(self, source_file):
        """
        Creates an Enfilade from a source file. Parses the source file to get info
        from it and stores the info as parameters here.
        """
        # Setup
        self.source_file = source_file
        self.references = defaultdict(lambda: [])

        # Parse document and get info
        print("parsing")
        paper_info = parser.parse(source_file)
        print("parsed")
        self.title = paper_info["title"]
        self.text = paper_info["text"]
        print("adding")
        self.add_citations(paper_info["citations"])
        print("added")

        # Convert document to images
        print("converting")
        self.imagedir = self.convert_to_images()
        print("converted")

    def add_citations(self, citation_list):
        """
        Reads in a list of citations for the document (provided by the parser)
        and stores them as data for the Enfilade. citation_list is a list of
        tuples (title, [page_numbers]) for every citation in the document.
        """
        # This will be a dictionary keyed by title, where the value is a list of
        # page numbers where that title is cited.
        for pair in citation_list:
            self.references[pair[0]] = pair[1]

    def convert_to_images(self):
        """
        Converts the stored pdf file to a directory of images. Returns image directory name.
        """
        # Prepare directory
        dirpath = os.path.join(
            os.path.dirname(self.source_file),
            pathlib.Path(self.source_file).stem + "_images"
        )
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        # Convert
        mat = fitz.Matrix(2.0, 2.0)
        doc = fitz.open(self.source_file)
        for i, page in enumerate(doc):
            # Create filename
            imagename = "page" + str(i) + ".jpg"
            path = os.path.join(dirpath, imagename)

            # Save
            pix = page.get_pixmap(matrix=mat)
            pix.save(path)

        return dirpath

    def get_citations(self):
        """
        Return a list of cited documents (not including the page numbers).
        """
        refs = [title for title in self.references]
        return refs

    def get_text(self):
        """Returns text of document"""
        return self.text

    def get_title(self):
        """Returns title of document"""
        return self.title

    def get_image_dir(self):
        """Returns image directory of document"""
        return self.imagedir

    def get_cited_pages(self, title):
        """
        Gets the page numbers where 'title' is cited
        """
        for ref in self.references:
            if title in ref:
                return self.references[ref]
        print("Error: not found")
        return [-1]


if __name__ == '__main__':
    testdoc = Enfilade("TestData/sciadv.abj2479.pdf")
    print(testdoc.references)
