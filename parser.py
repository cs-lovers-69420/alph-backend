# Contains functions for parsing research papers and returning information about
# the papers, such as title, authors, and citations to other papers.

from collections import defaultdict
from fileinput import filename
import os
import re
import pdftitle
import requests
import pdfplumber
from bs4 import BeautifulSoup

from pdfminer.high_level import extract_pages
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

    return ret


def _parse_pdf(filepath):
    """Parses a pdf file"""
    refs = []
    if False:
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
    # print(title)

    # Determine where citations are in the document and associate a list of
    # page numbers with each citation. Create a dictionary keyed by citation number
    page_dict = defaultdict(lambda: [])
    expr = r"(?:\(|\[)(\d+(?:,\s\d+)*)(?:\)|\])"
    pages = list(extract_pages(filepath))
    # Iterate through all pages
    for i, page in enumerate(pages[:1]):
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
                    elif "-" in cit:
                        # Create a range of numbers
                        nums = cit.split("-")
                        nums = list(range(int(nums[0]), int(nums[1])))
                        unique_cits.extend(nums)
                    else:
                        unique_cits.append(int(cit))
                unique_cits = list(set(unique_cits))

                # Add each citation to the page dictionary
                for cit in unique_cits:
                    page_dict[cit].append(i)

    print(page_dict)
    # with pdfplumber.open(filepath) as pdf:
    #     print("Starting loop")
    #     page = pdf.pages[0]
    #     text = page.extract_text(layout=True)
    #     print(text)
    #     citations = re.findall(expr, text)
    #     print(citations)
    # for i in range(reader.numPages):
    #     print(f"Getting page {i}")
    #     page = reader.getPage(i)
    #     text = page.extractText()
    #     citations = re.findall(expr, text)
    #     print(citations)

    # Associate a list of cited pages for each reference
    refs = [(ref, page_dict[i+1]) for i, ref in enumerate(refs)]
    print(refs)
    # print(refs[0])

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
    parse(
        "TestData/sciadv.abj2479.pdf")
    # parse(
    #     "TestData/3171221.3171289.pdf")
    # parse("TestData/Rasmussen2011_Article_AnOpenSystemFrameworkForIntegr.pdf")
