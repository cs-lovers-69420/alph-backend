# Contains functions for parsing research papers and returning information about
# the papers, such as title, authors, and citations to other papers.

from collections import defaultdict
import os
import re
import pdftitle
import requests
import pdfplumber
from bs4 import BeautifulSoup

from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer


def _parse_html(filepath):
    """
    Gets information from an html file (TODO: add hyperlink functionality?)
    NOTE: Might need to modify for paper links, but vast majority of functionality probably
    going to be PDFs.
    """
    title = ""  # Title of paper (FIXME)
    authors = []  # Authors of paper (TODO: get by regex search maybe?)
    citations = []  # Titles of cited works with page refs for where they appear

    # Get file
    if not os.path.exists(filepath):
        print("Path doesn't exist")
        return
    html = open(filepath)
    soup = BeautifulSoup(html, 'html.parser')

    # Get title from HTML title (NOTE: might not work?)
    title = soup.title.string

    # Get all links and titles of webpages they correspond to
    # TODO: If adding hyperlink functionality, might want to return links instead of titles
    all_links = [tag['href'] for tag in soup.select('p a[href]')]
    for link in all_links:
        response = requests.get(link)
        citations.append((BeautifulSoup(
            response.text, "html.parser").title.string, -1))

    print(citations)

    ret = defaultdict(lambda: None)
    ret["title"] = title
    ret["authors"] = authors
    ret["citations"] = citations
    ret["text"] = soup.get_text()

    return ret


def _parse_pdf(filepath):
    """Parses a pdf file"""
    refs = []
    with open(filepath, 'rb') as pdffile:
        # Get citations from the scholarcy API
        resp = requests.post(
            "https://ref.scholarcy.com/api/references/extract",
            files={'file': (filepath, pdffile, 'application/pdf')})
        refs = resp.json()['references']
        if len(refs) == 0:
            print("Error finding references")
            return

    # Get title from PDF
    # NOTE: This seems to work for most PDFs I've tried, but it's possible it won't
    # work for every PDF
    pdftitle.MISSING_CHAR = " "
    title = pdftitle.get_title_from_file(filepath)

    # Determine where citations are in the document and associate a list of
    # page numbers with each citation. Create a dictionary keyed by citation number
    page_dict = defaultdict(lambda: [])
    expr = r"(?:\(|\[)((?:\d+(?:,\s\d+)*)|(?:\d+(?:[-–—]\d+)?))(?:\)|\])"
    # Iterate through all pages
    for i, page in enumerate(extract_pages(filepath)):
        # Get all text on each page
        for element in page:
            if isinstance(element, LTTextContainer):
                # Get all citations on page
                text = element.get_text()
                citations = re.findall(expr, text)
                print(citations)

                # Process list to get a list of unique citations
                # If citation is of the form "(x, y)" or "(x-y)", replace with relevant numbers
                unique_cits = []
                for cit in citations:
                    if "," in cit:
                        # Split into a list of numbers and add this list to unique_cits
                        nums = cit.split(",")
                        nums = [int(n.strip()) for n in nums]  # Convert to int
                        unique_cits.extend(nums)
                    # Check for all types of dashes
                    elif re.search(r"[-–—]", cit):
                        # Create a range of numbers
                        nums = re.split(r"[-–—]", cit)
                        nums = list(range(int(nums[0]), int(nums[1])))
                        unique_cits.extend(nums)
                    else:
                        # Make sure not to add years
                        cit = int(cit)
                        if cit <= len(refs):
                            unique_cits.append(cit)
                unique_cits = list(set(unique_cits))

                # Add each citation to the page dictionary
                for cit in unique_cits:
                    page_dict[cit].append(i)

    # print(page_dict)

    # Associate a list of cited pages for each reference
    refs = [(ref, page_dict[i+1]) for i, ref in enumerate(refs)]
    print(refs)

    ret = defaultdict(lambda: None)
    ret["title"] = title
    ret["authors"] = []  # TODO: Are authors necessary?
    ret["citations"] = refs
    ret["text"] = extract_text(filepath)
    return ret


def _parse_test(filepath):
    """
    "Dummy" parser used in the test script.
    """
    ret = defaultdict(lambda: None)
    ret["title"] = os.path.basename(filepath)
    ret["authors"] = []
    ret["citations"] = []
    return ret


def parse(filepath):
    """
    Function called externally to parse a file. Calls either the html or pdf parser
    depending on filepath.
    """
    # Verify that path exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"'{filepath}' does not exist")

    if filepath.endswith(".html"):
        return _parse_html(filepath)
    elif filepath.endswith(".pdf"):
        return _parse_pdf(filepath)
    else:
        return _parse_test(filepath)


if __name__ == '__main__':
    parse(
        "TestData/sciadv.abj2479.pdf")
    # parse(
    #     "TestData/3171221.3171289.pdf")
    # parse("TestData/Rasmussen2011_Article_AnOpenSystemFrameworkForIntegr.pdf")
