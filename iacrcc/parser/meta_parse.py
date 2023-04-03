"""
Library for handling output meta file from compiling latex.
"""

import argparse
import json
from nameparser import HumanName
from pathlib import Path
from pylatexenc import latexwalker
from pylatexenc.latex2text import LatexNodes2Text, get_default_latex_context_db, MacroTextSpec
import re

def get_key_val(line):
    """If line has form key: value, then return key, value."""
    colon = line.find(':')
    if colon < 0:
        raise Exception('Exception: missing colon: {}'.format(line))
    key = line[:colon].strip()
    val = line[colon+1:].strip()
    return key, val
    
def _raise_lt_unknown_macro(n):
    """Callback for unknown macro or environment."""
    if n.isNodeType(latexwalker.LatexMacroNode):
        raise ValueError("Metadata may not contain unknown macro: '\\{}'".format(n.macroname))
    elif n.isNodeType(latexwalker.LatexEnvironmentNode):
        raise ValueError("Unknown environment: '\\begin{{{}}}'".format(n.environmentname))
    raise ValueError("Unknown latex construct: '{}'".format(n.latex_verbatim()))

def frac_decoder(n, l2tobj):
    """Better formatting for \frac."""
    arg1 = l2tobj.nodelist_to_text([n.nodeargd.argnlist[0]])
    arg2 = l2tobj.nodelist_to_text([n.nodeargd.argnlist[1]])
    return arg1 + '/' + arg2
    ans = ''
    if len(arg1) == 1:
        ans += arg1 + '/'
    else:
        ans += '(' + arg1 + ')/'
    if len(arg2) == 1:
        ans += arg2
    else:
        ans += '(' + arg2 + ')'
    return ans

def get_decoder():
    r"""Special handling for output from \protected@write."""
    lt_context_db = get_default_latex_context_db()
    lt_context_db.add_context_category('stripper',
                                       macros=[MacroTextSpec('texttt', '%s'),
                                               MacroTextSpec('textsf', '%s'),
                                               MacroTextSpec('it', ''),
                                               MacroTextSpec('frac', simplify_repl=frac_decoder),
                                               MacroTextSpec('protect', ''),
                                               MacroTextSpec('\\', ' '),
                                               MacroTextSpec('bot', '⊥'),
                                               MacroTextSpec('gcd', r'\gcd'),
                                               MacroTextSpec('sc', ''),
                                               MacroTextSpec('boldmath', ''),
                                               MacroTextSpec('bm', ''),
                                               MacroTextSpec('sl', '')],
                                       prepend=True)
    lt_context_db.set_unknown_macro_spec(MacroTextSpec('',
                                                       simplify_repl=_raise_lt_unknown_macro))
    return LatexNodes2Text(math_mode='with-delimiters',
                           strict_latex_spaces=True,
                           keep_braced_groups=True,
                           keep_comments=False,
                           latex_context=lt_context_db)

def remove_macros(txt):
    txt = txt.replace(r'\\[\s]+', ' ')
    txt = re.sub(r'\\thanks  {[^}]*} ?', '', txt)
    txt = re.sub(r'\\index  {[^}]*}', '', txt)
#    re.sub(r'\\protect (\\[a-zA-Z]+ )', r'THERE \1 HERE', txt)
    if re.match(r'\\protect \$ ', txt):
        re.sub(r'\\protect \$ ', r'\$', txt)
    return txt.strip()

def parse_meta(metastr):
    """Read the meta file line by line. When we encounter author: or affiliation: or title: or
       citation: we know how to process subsequent lines that start with two spaces.
    args:
       metastr: UTF-8 string from a .meta file.
    Returns:
        a dict with authors, affiliations, citations and (optionally) editors
    # TODO: define a JSON schema for this file, or return a pydantic object.
    """
    decoder = get_decoder()
    data = {'authors': [],
            'affiliations': [],
            'funders': [],
            'citations': []}

    lines = metastr.splitlines()
    numlines = len(lines)
    index = 0
    while index < numlines:
        line = lines[index].rstrip()
        if line.startswith('author:'):
            author = {'affiliations': []}
            data['authors'].append(author)
            index = index + 1
            while index < numlines and lines[index].startswith('  '):
                k,v = get_key_val(lines[index].rstrip())
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
                elif k == 'email':
                    author['email'] = v
                elif k == 'affil':
                    author['affiliations'] = [a for a in v.split(',' ) if a.isnumeric()]
                elif k == 'orcid':
                    author['orcid'] = v.rstrip()
                index += 1
        elif line.startswith('affiliation:'):
            affiliation = {}
            data['affiliations'].append(affiliation)
            index += 1
            while index < numlines and lines[index].startswith('  '): # associated with affiliation
                k,v = get_key_val(lines[index])
                affiliation[k] = decoder.latex_to_text(v)
                index += 1
        elif line.startswith('funding:'):
            funder = {}
            data['funders'].append(funder)
            index += 1
            while index < numlines and lines[index].startswith('  '):
                k,v = get_key_val(lines[index])
                funder[k] = decoder.latex_to_text(v)
                index += 1
        elif line.startswith('version:'):
            data['version'] = line[8:].strip()
            index += 1
        elif line.startswith('title:'):
            data['title'] = decoder.latex_to_text(line[6:].strip())
            index += 1
            if index < numlines and lines[index].startswith('  '):
                k,v = get_key_val(lines[index])
                if k == 'subtitle':
                    data['subtitle'] = v
                    index += 1
        elif line.startswith('keywords:'):
            data['keywords'] = [k.strip() for k in decoder.latex_to_text(line[9:].strip()).split(',')]
            index += 1
        elif line.startswith('citation:'):
            parts = line.split()
            assert(len(parts) == 3)
            citation = {'ptype': parts[1].strip(),
                        'id': parts[2].strip(),
                        'authorlist': []}
            data['citations'].append(citation)
            index += 1
            while index < numlines and lines[index].startswith('  '): # associated with citation:
                k,v = get_key_val(lines[index])
                if k == 'authors': # Original BibTeX form.
                    citation['authors'] = decoder.latex_to_text(v)
                    index += 1
                elif k == 'author': # separated out by bst
                    author = {'name': decoder.latex_to_text(v)}
                    citation['authorlist'].append(author)
                    index += 1
                    k,v = get_key_val(lines[index])
                    if k == 'surname':
                        author['surname'] = decoder.latex_to_text(v)
                        index += 1
                elif k == 'editor':
                    if 'editors' not in citation:
                        citation['editors'] = []
                    editor = {'name': v}
                    citation['editors'].append(editor)
                    index += 1
                    k,v = get_key_val(lines[index])
                    if k == 'surname':
                        editor['surname'] = v
                        index += 1
                else:
                    citation[k] = v
                    index += 1
        else:
            raise Exception('unexpected line {}'.format(line))
    return data

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Parse a meta file')
    argparser.add_argument('--input_file',
                           required=True,
                           help='meta file to parse')
    args = argparser.parse_args()
    metafile = Path(args.input_file)
    mstr = metafile.read_text(encoding='UTF-8')
    metadata = parse_meta(mstr)
    print(json.dumps(metadata, indent=2))
