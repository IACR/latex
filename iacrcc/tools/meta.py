#!/usr/bin/python3
"""
This is designed to read the .meta file and produce three possible outputs, depending on
which command line arguments are used:
 * .json file with structured version of .meta file
 * .xml file for reporting to crossref
 * .xmp file with citations for inclusion in PDF (TBD)

See the README.md in this directory.

TODO: generate tests for this binary.
"""

import argparse
import datetime
from enum import IntEnum
from pathlib import Path
import pypandoc
import json
import re
import sys
from pylatexenc.latex2text import LatexNodes2Text
from nameparser import HumanName
from xml.etree import ElementTree as ET
from xml.dom import minidom
import latex2mathml.converter

class ExitCodes(IntEnum):
    MISSING_ARGS = 1
    MISSING_DOI = 2
    MISSING_TITLE = 3
    MISSING_ABSTRACT = 3
    
# This is used to decode lines with TeX character macros like \'e.
decoder = LatexNodes2Text()

def _pretty_print_xml(root):
    """Pretty-print an ElementTree root."""
    return minidom.parseString(ET.tostring(root, encoding='unicode', xml_declaration=True)).toprettyxml(indent = "   ")

def get_key_val(line):
    """If line has form key: value, then return key, value."""
    colon = line.find(':')
    if colon < 0:
        raise Exception('Exception: missing colon: {}'.format(line))
    key = line[:colon].strip()
    val = line[colon+1:].strip()
    return key, val
    

def title_to_jats(node, title):
    """Attach article-title to element-citation node in JATS format. This is
       used for XMP output.

      Parameters:
        node: an xml.etree.ElementTree Element to attach 'article-title' element.
        title: the string with mixed TeX content with text and inline math.

    TODO: switch XMP to use mathml (and add namespace for it).
    """
    delims = ['$', '\\(', '\\)']
    # This splits the string into parts by the delimiters $, \(, and \)
    parts = re.split(r'([\\][()]|[$])',title)
    inmath = False
    encoded = '<article-title>'
    for i in range(len(parts)):
        if parts[i] in delims:
            inmath = not inmath
        else:
            if inmath:
                # for math, just the raw TeX.
                # TODO: switch to mathml, since latex needs to be inside CDATA and
                # ElementTree does not support CDATA.
                #
                encoded += '<tex-math>' + parts[i] + '</tex-math>'
            else:
                # for non-math, just character codes
                encoded += decoder.latex_to_text(parts[i])
    encoded += '</article-title>'
    tnode = ET.fromstring(encoded)
    node.append(tnode)

def title_to_utf8(title):
    """Very simple conversion of title to UTF-8. This doesn't handle superscripts and
       subscripts, leaving them as ^ and _. Intended for citation titles in crossref."""
    return decoder.latex_to_text(title)

def title_to_crossref(elem_name, title):
    """Convert titles to an Element with mathml for inline math. This is used for
    crossref format.

    The conversion is tricky, because title may contain inline mathematics but it
    may also contain TeX control characters in text mode. We split the string into
    math and text pieces using a regular expression. Then we use latex2mathml to convert
    the inline math and pylatenxnc to convert the text fragments.

    Parameters:
      elem_name: name for the root node
      title: LaTeX string for title.
    Returns:
      string representation of xml for crossref, containing mathml.
    TODO: develop some tests for this
    """
    delims = ['$', '\\(', '\\)']
    # This splits the string into parts by the delimiters $, \(, and \)
    parts = re.split(r'([\\][()]|[$])',title)
    encoded = ''
    inmath = False
    for i in range(len(parts)):
        if parts[i] in delims:
            inmath = not inmath
        else:
            if inmath:
                # for math
                encoded += latex2mathml.converter.convert(parts[i])
            else:
                # for non-math, just character codes
                encoded += decoder.latex_to_text(parts[i])
    encoded = '<{}>{}</{}>'.format(elem_name, encoded, elem_name)
    return encoded

def _add_jats_ref(citation, reflist):
    """Used for adding a ref node in JATS format for citations."""
    ref = ET.SubElement(reflist, 'ref', attrib={'id': citation['id']})
    cite_node = ET.SubElement(ref, 'element-citation',
                              attrib={'publication-type': citation['type']})
    return cite_node

def add_jats_persons(cite_node, persons):
    """Either add editors or authors as <person> nodes.

       Parameters:
         cite_node: an xml.etree.ElementTree.Element to attach <person> nodes.
         persons: an array of person dicts with 'name' in them.
       Returns:
         nothing, but cite_node is appended to.
    """
    for person in persons:
        person_node = ET.SubElement(cite_node, 'person')
        humanname = HumanName(person['name'])
        given = ''
        if humanname.first:
            given = humanname.first
            if humanname.middle:
                given += ' ' + humanname.middle
            ET.SubElement(person_node, 'given-names').text = given
        if humanname.last:
            ET.SubElement(person_node, 'surname').text = humanname.last
        else:
            ET.SubElement(person_node, 'surname').text = person['name']
        
def _report_error(level, msg):
    """TODO: switch to the logging package."""
    print('{}:{}'.format(level, msg))
    
def add_jats_article(citation, reflist):
    """Process a dict with bibtex fields for an article.
       Parameters:
         citation: a dict that requires 'title', 'journal', and 'authorlist'
         reflist: Element for 'ref-list'
       Returns:
         nothing, but reflist is appended to.
    """
    if 'title' in citation and 'journal' in citation and citation['authorlist']:
        cite_node = _add_jats_ref(citation, reflist)
        title_to_jats(cite_node, citation['title'])
        ET.SubElement(cite_node, 'source').text = citation['journal']
        add_jats_persons(cite_node, citation['authorlist'])
        if 'year' in citation:
            ET.SubElement(cite_node, 'year').text = citation['year']
        if 'month' in citation:
            ET.SubElement(cite_node, 'month').text = citation['month']
        if 'volume' in citation:
            ET.SubElement(cite_node, 'volume').text = citation['volume']
        if 'issue' in citation:
            ET.SubElement(cite_node, 'issue').text = citation['issue']
        if 'pages' in citation:
            # Just the first page
            parts = citation['pages'].split('-')
            ET.SubElement(cite_node, 'fpage').text = parts[0]
        if 'note' in citation:
            ET.SubElement(cite_node, 'comment').text = citation['note']
    else:
        report_error('warning',
                     'Missing fields in article[{}]'.format(citation.get('key', '?')))
            
def add_jats_book(citation, reflist):
    """Process a dict with bibtex book fields.
       Parameters:
         citation: a dict with bibtex fields. Should contain 'title', 'publisher', 'year', and
                   either 'author' or 'editor'
         reflist: Element to append 'jats:ref' to.
    """
    if 'title' in citation and 'year' in citation and 'publisher' in citation and (citation['authorlist'] or 'editors' in citation):
        cite_node = _add_jats_ref(citation, reflist)
        ET.SubElement(cite_node, 'source').text = decoder.latex_to_text(citation['title'])
        ET.SubElement(cite_node, 'year').text = citation['year']
        ET.SubElement(cite_node, 'publisher-name').text = citation['publisher']
        if 'address' in citation:
            ET.SubElement(cite_node, 'publisher-loc').text = citation['address']
        if citation['authorlist']:
            add_jats_persons(cite_node, citation['authorlist'])
        else:
            add_jats_persons(cite_node, citation['editors'])
        if 'month' in citation:
            ET.SubElement(cite_node, 'month').text = citation['month']
        if 'edition' in citation:
            ET.SubElement(cite_node, 'edition').text = citation['edition']
        if 'note' in citation:
            ET.SubElement(cite_node, 'comment').text = citation['note']
    else:
        report_error('warning',
                     'Missing fields in book[{}]'.format(citation.get('key', '?')))

def add_jats_inproceedings(citation, reflist):
    # title, booktitle, and authors are required. Should also have year
    if 'title' in citation and 'booktitle' in citation and citation['authorlist']:
        cite_node = _add_jats_ref(citation, reflist)
        #nodes = ET.fromstring(latex2mathml.converter.convert(citation['title']))
        title_to_jats(cite_node, citation['title'])
        ET.SubElement(cite_node, 'source').text = citation['booktitle']
        add_jats_persons(cite_node, citation['authorlist'])
        if 'year' in citation:
            ET.SubElement(cite_node, 'year').text = citation['year']
        if 'month' in citation:
            ET.SubElement(cite_node, 'month').text = citation['month']
        if 'series' in citation:
            ET.SubElement(cite_node, 'volume').text = citation['volume']
        if 'pages' in citation:
            # Just the first page
            parts = citation['pages'].split('-')
            ET.SubElement(cite_node, 'fpage').text = parts[0]
        if 'note' in citation:
            ET.SubElement(cite_node, 'comment').text = citation['note']

def add_jats_generic(citation, reflist):
    """Add all nodes that we can that make sense."""
    cite_node = _add_jats_ref(citation, reflist)
    if 'title' in citation:
        ET.SubElement(cite_node, 'source').text = decoder.latex_to_text(citation['title'])
    elif 'booktitle' in citation:
        ET.SubElement(cite_node, 'source').text = citation['booktitle']
    if citation['authorlist']:
        add_jats_persons(cite_node, citation['authorlist'])
    elif 'editors' in citation:
        add_jats_persons(cite_node, citation['editors'])
    if 'year' in citation:
        ET.SubElement(cite_node, 'year').text = citation['year']
    if 'month' in citation:
        ET.SubElement(cite_node, 'month').text = citation['month']
    if 'volume' in citation:
        ET.SubElement(cite_node, 'volume').text = citation['volume']
    if 'issue' in citation:
        ET.SubElement(cite_node, 'issue').text = citation['issue']
    if 'pages' in citation:
        # Just the first page
        parts = citation['pages'].split('-')
        ET.SubElement(cite_node, 'fpage').text = parts[0]
    if 'address' in citation:
        ET.SubElement(cite_node, 'publisher-loc').text = citation['address']
    if 'chapter' in citation:
        ET.SubElement(cite_node, 'chapter-title').text = citation['chapter']
    if 'edition' in citation:
        ET.SubElement(cite_node, 'edition').text = citation['edition']
    if 'howpublished' in citation:
        ET.SubElement(cite_node, 'comment').text = citation['howpublished']
    if 'note' in citation:
        ET.SubElement(cite_node, 'comment').text = citation['note']
    if 'publisher' in citation:
        ET.SubElement(cite_node, 'publisher-name').text = citation['publisher']
    elif 'organization' in citation:
        ET.SubElement(cite_node, 'publisher-name').text = citation['organization']
    elif 'school' in citation:
        ET.SubElement(cite_node, 'publisher-name').text = citation['school']
    if 'address' in citation:
        ET.SubElement(cite_node, 'publisher-loc').text = citation['address']
    if 'pages' in citation:
        # Just the first page
        parts = citation['pages'].split('-')
        ET.SubElement(cite_node, 'fpage').text = parts[0]
         

def _crossref_batch_info():
    """Return batch_id, timestamp for crossref deposit format."""
    now = datetime.datetime.now(datetime.timezone.utc)
    return now.strftime('IACRCC:%Y%m%d:%H%M%S'), now.strftime('%Y%m%d%H%M%S')


def read_meta(metafile):
    """Read the meta file line by line. When we encounter author: or affiliation: or title: or
       citation: we know how to process subsequent lines that start with two spaces.
       Returns:
          a dict with authors, affiliations, citations and (optionally) editors
    # TODO: define a JSON schema for this file.
    """
    data = {'authors': [],
            'affiliations': [],
            'citations': []}

    with metafile.open() as f:
        line = f.readline().rstrip()
        while line:
            if line.startswith('author:'):
                author = {}
                data['authors'].append(author)
                line = f.readline().rstrip()
                while line.startswith('  '): # associated with author
                    k,v = get_key_val(line)
                    if k == 'name':
                        author[k] = v
                        v = decoder.latex_to_text(v)
                        parsed = HumanName(v)
                        if parsed:
                            author[k] = str(parsed) # canonicalize name
                            if parsed.last:
                                author['surname'] = parsed.last
                            if parsed.first:
                                author['given'] = parsed.first
                        else: # surname is required, so guess if the parser fails.
                            parts = author[k].split()
                            author['surname'] = parts[-1]
                    elif k == 'affil':
                        author['affiliations'] = v
                    line = f.readline().rstrip()
            elif line.startswith('affiliation:'):
                affiliation = {}
                data['affiliations'].append(affiliation)
                line = f.readline().rstrip()
                while line.startswith('  '): # associated with affiliation
                    k,v = get_key_val(line)
                    affiliation[k] = decoder.latex_to_text(v)
                    line = f.readline().rstrip()
            elif line.startswith('title:'):
                data['title'] = line[6:].strip()
                line = f.readline().rstrip()
                if line.startswith('  '):
                    k,v = get_key_val(line)
                    if k == 'subtitle':
                        data['subtitle'] = v
                        line = f.readline().rstrip()
            elif line.startswith('keywords:'):
                data['keywords'] = line[9:].strip()
                line = f.readline().rstrip()
            elif line.startswith('citation:'):
                parts = line.split()
                assert(len(parts) == 3)
                citation = {'type': parts[1].strip(),
                            'id': parts[2].strip(),
                            'authorlist': []}
                data['citations'].append(citation)
                line = f.readline().rstrip()
                while line.startswith('  '): # associated with citation:
                    k,v = get_key_val(line)
                    if k == 'authors': # Original BibTeX form.
                        citation['authors'] = decoder.latex_to_text(v)
                        line = f.readline().rstrip()
                    elif k == 'author': # separated out by bst
                        author = {'name': decoder.latex_to_text(v)}
                        citation['authorlist'].append(author)
                        line = f.readline().rstrip()
                        k,v = get_key_val(line)
                        if k == 'surname':
                            author['surname'] = decoder.latex_to_text(v)
                            line = f.readline().rstrip()
                    elif k == 'editor':
                        if 'editors' not in citation:
                            citation['editors'] = []
                        editor = {'name': v}
                        citation['editors'].append(editor)
                        line = f.readline().rstrip()
                        k,v = get_key_val(line)
                        if k == 'surname':
                            editor['surname'] = v
                            line = f.readline().rstrip()
                    else:
                        citation[k] = v
                        line = f.readline().rstrip()
            else:
                raise Exception('unexpected line {}'.format(line))
    return data

def add_citation_node(citation_list, citation):
    """Add a <citation> node to citation_list for crossref.
    Parameters:
      citation_list: Element containing the <citation> elements
      citation: dict containing fields of the citation.
      TODO: insert more elements to comply with schema.
    """
    if 'doi' in citation:
        # used to create string titles.
        dummy_node = ET.Element('junk')
        # for now we only add them if there is a DOI.
        cite_node = ET.SubElement(citation_list, 'citation',
                                  attrib={'key': citation['id']})
        ET.SubElement(cite_node, 'doi').text = citation['doi']
        # fields that apply to all types
        if 'url' in citation:
            ET.SubElement(cite_node, 'elocation_id').text = citation['url']
        if 'authorlist' in citation:
            # this is dumb. They only take the surname of the first author for matching.
            ET.SubElement(cite_node, 'author').text = citation['authorlist'][0]['surname']
        if 'year' in citation:
            # yes, it's called cYear.
            ET.SubElement(cite_node, 'cYear').text = citation['year']
        if citation['type'] == 'article':
            if 'issn' in citation:
                ET.SubElement(cite_node, 'issn').text = citation['issn']
            if 'journal' in citation:
                ET.SubElement(cite_node, 'journal_title').text = citation['journal']
            if 'title' in citation:
                ET.SubElement(cite_node, 'article_title').text = title_to_utf8(citation['title'])
            if 'volume' in citation:
                ET.SubElement(cite_node, 'volume').text = citation['volume']
            if 'number' in citation:
                ET.SubElement(cite_node, 'issue').text = citation['number']
            if 'pages' in citation:
                ET.SubElement(cite_node, 'first_page').text = citation['pages'].split('-')[0]
        elif citation['type'] == 'inproceedings':
            if 'isbn' in citation:
                ET.SubElement(cite_node, 'isbn').text = citation['isbn']
            if 'booktitle' in citation:
                ET.SubElement(cite_node, 'volume_title').text = citation['booktitle']
            if 'title' in citation:
                ET.SubElement(cite_node, 'article_title').text = citation['title']
            if 'volume' in citation:
                ET.SubElement(cite_node, 'volume').text = citation['volume']
            if 'series' in citation:
                ET.SubElement(cite_node, 'series_title').text = citation['series']
            if 'number' in citation:
                ET.SubElement(cite_node, 'issue').text = citation['number']
            if 'pages' in citation:
                ET.SubElement(cite_node, 'first_page').text = citation['pages'].split('-')[0]
        elif citation['type'] == 'book':
            if 'isbn' in citation:
                ET.SubElement(cite_node, 'isbn').text = citation['isbn']
            if 'title' in citation:
                ET.SubElement(cite_node, 'volume_title').text = citation['title']
        else: # generic type, like misc or inbook or manual or techreport
            if 'title' in citation:
                ET.SubElement(cite_node, 'article_title').text = citation['title']
                

def create_crossref(args, data):
    """Save crossref deposit format. This adheres to schema version 5.3.1
       See https://data.crossref.org/reports/help/schema_doc/5.3.1/index.html
       and https://gitlab.com/crossref/schema/-/blob/master/best-practice-examples/journal.article5.3.0.xml
    """
    # Note: latex2mathml uses no namespace prefix, so we have to add this.
    ET.register_namespace('m', 'http://www.w3.org/1998/Math/MathML')
    ET.register_namespace('jats', 'http://www.ncbi.nlm.nih.gov/JATS1')
    root = ET.Element('doi_batch', attrib={'xmlns': 'http://www.crossref.org/schema/5.3.1',
                                           'xsi:schemaLocation': 'http://www.crossref.org/schema/5.3.1 https://www.crossref.org/schemas/crossref5.3.1.xsd',
                                           'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                           'xmlns:fr': 'http://www.crossref.org/fundref.xsd',
                                           'version': '5.3.1'})
    head = ET.SubElement(root, 'head')
    batch_id, ts = _crossref_batch_info()
    if args.crossref_batch_id:
        ET.SubElement(head, 'doi_batch').text = args.crossref_batch_id
    else:
        ET.SubElement(head, 'doi_batch_id').text = batch_id
    ET.SubElement(head, 'timestamp').text = ts
    depositor = ET.SubElement(head, 'depositor')
    ET.SubElement(depositor, 'depositor_name').text = 'IACR'
    ET.SubElement(depositor, 'email_address').text = 'crossref@iacr.org'
    ET.SubElement(head, 'registrant').text = 'International Association for Cryptologic Research'
    body = ET.SubElement(root, 'body')
    journal = ET.SubElement(body, 'journal')
    journal_metadata = ET.SubElement(journal, 'journal_metadata',
                                     attrib={'language': 'en',
                                             'reference_distribution_opts': 'any'})
    ET.SubElement(journal_metadata, 'full_title').text = 'IACR Communications on Cryptology'
    ET.SubElement(journal_metadata, 'abbrev_title').text = 'IACR CC'
    ET.SubElement(journal_metadata, 'issn', attrib={'media_type': 'electronic'}).text = '1234-5678'
    archive_locations = ET.SubElement(journal_metadata, 'archive_locations')
    # TODO: should we use Portico, CLOCKSS, DWT, KB, or LOCKSS?
    ET.SubElement(archive_locations, 'archive', attrib={'name': 'Internet Archive'})
    # TODO: insert doi_data for journal (not journal_article?)
    pub_type = 'bibliographic_record'
    # TODO: once we start reporting abstract, switch to this:
    # pub_type = 'abstract_only' if args.abstract else 'bibliographic_record'
    journal_article = ET.SubElement(journal, 'journal_article',
                                    attrib={'language': 'en',
                                            'publication_type': pub_type,
                                            'reference_distribution_opts': 'any'})
    titles = ET.SubElement(journal_article, 'titles')
    titles.append(ET.fromstring(title_to_crossref('title', data['title'])))
    if 'subtitle' in data:
        titles.append(ET.fromstring(title_to_crossref('subtitle', data['subtitle'])))
    contributors = ET.SubElement(journal_article, 'contributors')
    for author in data['authors']:
        # Note: 'first' does not mean what you think it is. You can have multiple 'first'
        # authors.
        person = ET.SubElement(contributors, 'person_name',
                               attrib = {'contributor_role': 'author', 'sequence': 'first'})
        # The validator rejected this element, but it seems to agree with the schema.
        # ET.SubElement(person, 'alt-name').text = author['name']
        if 'given' in author:
            ET.SubElement(person, 'given_name').text = author['given']
        ET.SubElement(person, 'surname').text = author['surname']
        if 'orcid' in author:
            # TODO: review policy on whether we will authenticate orcid IDs.
            ET.SubElement(person, 'ORCID', attrib={'authenticated': "false"}).text = 'https://orcid.org/' + author['orcid']
        if 'affiliations' in author:
            affil_list = author['affiliations'].split(',')
            if len(affil_list):
                affiliations = ET.SubElement(person, 'affiliations')
                for index in affil_list:
                    if index.isdigit():
                        index = int(index)
                        if 0 < index <= len(data['affiliations']):
                            affiliation = data['affiliations'][index - 1]
                            institution_node = ET.SubElement(affiliations, 'institution')
                            ET.SubElement(institution_node, 'institution_name').text = affiliation['name']
                            if 'ror' in affiliation:
                                ror = affiliation['ror']
                                if not ror.startswith('http'): # it might be just the id
                                    ror = 'https://ror.org/' + ror
                                ET.SubElement(institution_node, 'institution_id',
                                              attrib={'type': 'ror'}).text = ror
    # TODO: figure out how to encode abstracts?
    # if 'abstract' in data:
    #        abstract_node = ET.SubElement(journal_article, 'abstract')
    #        ET.SubElement(abstract_node, 'jats:p', attrib={'xml:lang': 'en'}).text = data['abstract']
    today = datetime.date.today()
    date_node = ET.SubElement(journal_article, 'publication_date', attrib={'media_type': 'online'})
    # Weirdly, it seems to expect these in order month, day, year
    ET.SubElement(date_node, 'month').text = str(today.month).zfill(2)
    ET.SubElement(date_node, 'day').text = str(today.day).zfill(2)
    ET.SubElement(date_node, 'year').text = str(today.year)

    # TODO: check mime_type, and make sure we are assigning to an existing web page.
    doi_data = ET.SubElement(journal_article, 'doi_data')
    ET.SubElement(doi_data, 'doi').text = args.doi
    ET.SubElement(doi_data, 'resource', attrib={'content_version': 'vor',
                                                'mime_type': 'text/html'}).text = 'https://cc.iacr.org/' + args.doi
    # Make sure there is at least one citation with a DOI
    if len([c for c in data['citations'] if 'doi' in c]):
        cite_list_node = ET.SubElement(journal_article, 'citation_list')
        for citation in data['citations']:
            add_citation_node(cite_list_node, citation)            
    crossref_path = Path(args.crossref)
    crossref_path.write_text(_pretty_print_xml(root), encoding='utf-8')

def main():
    argparser = argparse.ArgumentParser(description='Process metadata from iacrcc')
    argparser.add_argument('--input',
                           required=True,
                           help='Path to .meta file for input')
    argparser.add_argument('--doi',
                           default='10.1234/12345',
                           help='DOI chosen from our namespace')
    argparser.add_argument('--abstract',
                           help='Path to optional abstract file extracted from iacrcc.cls')
    argparser.add_argument('--citations',
                           help='Filename to export XMP file for citations')
    argparser.add_argument('--json',
                           help='Filename to export JSON file.')
    argparser.add_argument('--crossref',
                           help='Filename to export crossref deposit XML file')
    argparser.add_argument('--crossref_batch_id',
                           help='Optional crossref batch_id')

    args = argparser.parse_args()
    if not args.citations and not args.json and not args.crossref:
        print('One of --citations, --json, or --crossref is required')
        sys.exit(ExitCodes.MISSING_ARGS.value)
        
    if args.crossref and not args.doi:
        print('--doi is required with --crossref')
        sys.exit(ExitCodes.MISSING_DOI.value)
    
    metafile = Path(args.input)
    if not metafile.is_file():
        print('missing file ' + metafile.name)
        sys.exit(EditCodes.MISSING_TITLE.value)
    data = read_meta(metafile)
    if args.abstract:
        abstractpath = Path(args.abstract)
        if not abstractpath.is_file():
            print('Missing abstract file {}'.format(args.abstract))
            sys.exit(ExitCodes.MISSING_ABSTRACT.value)
        data['abstract'] = abstractpath.read_text(encoding='utf-8')
        data['abstract'] = pypandoc.convert_text(data['abstract'], 'jats', 'latex')

    if args.json:
        jsonfile = Path(args.json)
        jsonfile.write_text(json.dumps(data, indent=2), encoding='utf-8')
    if args.crossref:
        create_crossref(args, data)
        
    if args.citations:
        # This prints an XMP file to the location args.citations.
        root = ET.Element('x:xmpmetadata', attrib={'xmlns:x':'adobe:ns:meta/'})
        tree = ET.ElementTree(root)
        root.insert(1, ET.Comment('This contains citations in the JATS 1.2 schema'))
        rdf = ET.SubElement(root, 'rdf:RDF', attrib={'xmlns': 'http://www.ncbi.nlm.nih.gov/JATS1'})
        reflist = ET.SubElement(rdf, 'ref-list')
        reftitle = ET.SubElement(reflist, 'title')
        reftitle.text = 'Bibliography'
        for citation in data['citations']:
            if citation['type'] == 'article':
                add_jats_article(citation, reflist)
            elif citation['type'] == 'book':
                add_jats_book(citation, reflist)
            elif citation['type'] == 'inproceedings':
                add_jats_inproceedings(citation, reflist)
            else:
                add_jats_generic(citation, reflist)
        tree.write(args.citations, encoding='UTF-8', xml_declaration=False)


if __name__ == "__main__":
    main()
