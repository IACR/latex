"""
Parser to extract XMP metadata from PDF. strings may be retrieved with xpath queries.
"""

from xml.etree import ElementTree as ET
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

class XMPParser(object):
    def __init__(self, pdf_file_path):
        self.namespaces = {
            'xmpRights': "http://ns.adobe.com/xap/1.0/rights/",
            'stFnt':    "http://ns.adobe.com/xap/1.0/sType/Font#",
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'xap': 'http://ns.adobe.com/xap/1.0/',
            'pdf': 'http://ns.adobe.com/pdf/1.3/',
            'xapmm': 'http://ns.adobe.com/xap/1.0/mm/',
            'pdfx': 'http://ns.adobe.com/pdfx/1.3/',
            'prism': 'http://prismstandard.org/namespaces/basic/3.0/',
            'crossmark': 'http://crossref.org/crossmark/1.0/',
            'rights': 'http://ns.adobe.com/xap/1.0/rights/',
            'xml': 'http://www.w3.org/XML/1998/namespace',
            'xmpTPg': 'http://ns.adobe.com/xap/1.0/t/pg/'
        }
        with open(pdf_file_path, 'rb') as fp:
            parser = PDFParser(fp)
            doc = PDFDocument(parser)
            metadata = resolve1(doc.catalog['Metadata']).get_data()
            self.root = ET.fromstring(metadata)
    def get_string(self, xpath):
        """xpath is an xpath query, e.g., './/dc:source'"""
        elem = self.root.find(xpath, self.namespaces)
        if elem is None:
            return None
        return elem.text
    def get_strings(self, xpath):
        """xpath is an xpath query, e.g., './/dc:source'"""
        elemlist = self.root.findall(xpath, self.namespaces)
        if elemlist is None:
            return []
        result = []
        for el in elemlist:
            result.append(el.text)
        return result

if __name__ == '__main__':
    parser = XMPParser('test11/main.pdf')
    authors = parser.get_strings('.//dc:creator/rdf:Seq/rdf:li')
    print(authors)
    title = parser.get_string('.//dc:title/rdf:Alt/rdf:li')
    print(title)
    description = parser.get_string('.//dc:description/rdf:Alt/rdf:li')
    print('description')
    print(description)
    marked = parser.get_string('.//xmpRights:Marked')
    print(marked)
    webStatement = parser.get_string('.//xmpRights:WebStatement')
    print(webStatement)
    rights = parser.get_string('.//dc:rights/rdf:Alt/rdf:li')
    print(rights)
    keywords = parser.get_string('.//pdf:Keywords')
    print(keywords)
    subject = parser.get_strings('.//dc:subject/rdf:Bag/rdf:li')
    print(subject)
    identifier = parser.get_string('.//dc:identifier')
    print(identifier)
    doi = parser.get_string('.//prism:doi')
    print(doi)
    pubname = parser.get_string('.//prism:publicationName')
    print(pubname)
    aggregation = parser.get_string('.//prism:aggregationType')
    print(aggregation)
