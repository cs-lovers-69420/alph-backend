# Contains functions for parsing research papers and returning information about
# the papers, such as title, authors, and citations to other papers.

from collections import defaultdict
import os
from queue import Empty
import re
import requests
import PyPDF2
import textract
from bs4 import BeautifulSoup


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

    return ret


def _parse_pdf(filepath):
    """Parses a pdf file"""
    # Open file for use later
    pdffile = open(filepath, 'rb')

    # Get citations from the scholarcy API
    resp = requests.post(
        "https://ref.scholarcy.com/api/references/extract",
        files={'file': (filepath, pdffile, 'application/pdf')})
    refs = resp.json()['references']
    if len(refs) == 0:
        print("Error finding references")
        return
    # print(refs)
    print(resp.json().keys())
    print(resp.json()['metadata'])

    # Get title from metadata by reading PDF
    # NOTE: This seems to work for most PDFs I've tried, but it's possible it won't
    # work for every PDF
    pdfReader = PyPDF2.PdfFileReader(pdffile)
    doc_info = pdfReader.getDocumentInfo()
    print(doc_info)
    title = doc_info["/Title"]

    # TODO: Determine where citations are in the document and associate a list of
    # page numbers with each citation. This isn't strictly necessary but could
    # be nice.
    refs = [(ref, -1) for ref in refs]
    print(refs[0])

    # # Get text that corresponds to citations
    # # NOTE: A different module is used that is better at handling the text
    # pdftext = textract.process(filepath).decode("utf-8")
    # # NOTE: Won't work if a cited paper has "references" in the title
    # # TODO: replace with regex if this doesn't work reliably
    # ind = pdftext.rfind("References")
    # if ind == -1:
    #     ind = pdftext.rfind("REFERENCES")
    # refs = pdftext[ind:]
    # # print(refs)

    # # Find all citations
    # # Starting with n=1: find citation n, get the citation, repeat for n+1 on the remaining
    # # references string not including the citation. Get citation by looking for next number.
    # # NOTE: won't work if citations aren't numbered. Is this ever the case? Idk.

    # # Determine what's to the left and right of the first number to find other numbers
    # re_specialchars = r".+*?^$()[]{}\|"
    # curr = 1
    # index = refs.find(str(curr))
    # left_char = refs[index-1]
    # right_char = refs[index+1]

    # # Need to escape special characters if included
    # if left_char in re_specialchars:
    #     left_char = "\\" + left_char
    # if right_char in re_specialchars:
    #     right_char = "\\" + right_char
    # expr = r"\s+" + left_char.strip() + r"\d+" + right_char.strip()
    # # print(expr)

    # citations = re.split(expr, refs)[1:]
    # print(citations[0])
    # print("\n\n")
    # print(citations[1])
    # print("\n\n")
    # print(citations[2])

    ret = defaultdict(lambda: None)
    ret["title"] = title
    ret["authors"] = []  # TODO: Are authors necessary?
    ret["citations"] = refs
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
    # parse(
    #     "TestData/sciadv.abj2479.pdf")
    # parse(
    #     "TestData/3171221.3171289.pdf")
    parse("TestData/Rasmussen2011_Article_AnOpenSystemFrameworkForIntegr.pdf")
