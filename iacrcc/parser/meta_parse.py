"""
Library for handling output meta file from compiling latex.

The exact syntax of the .meta file is a little unclear. The TeXbook
states on page 228 that
  ``Each write command produces output in the form that TeX always uses to display
    token lists symbolically: Characters represent themselves (except that you get
    duplicated characers like ## for macro parameter characters); unexpandable control
    sequence tokens produce their names, preceded by the \\escapechar and followed by a
    space (unless the name is an active character or a control sequence formed from a
    single nonletter).''
That seems to imply that \\$ and \\% are special cases. Indeed the handling of \\$ changed
in texlive 2025 (perhaps due to this: https://github.com/latex3/latex2e/pull/1388).
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

class LatexToText(LatexNodes2Text):
    """There are some things that LatexNodes2Text cannot handle, like
       removing T1 (it doesn't recognize those as a macro)."""
    def _preclean(self, text):
        return text.replace('\\T1', '')
    def latex_to_text(self, v):
        return super().latex_to_text(self._preclean(v))

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
                                               MacroTextSpec('sl', ''),
                                               MacroTextSpec('TU', '')],
                                       prepend=True)
    lt_context_db.set_unknown_macro_spec(MacroTextSpec('',
                                                       simplify_repl=_raise_lt_unknown_macro))
    return LatexToText(math_mode='with-delimiters',
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


def validate_orcid(orcid):
    """Implements algorithm on https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier"""
    if not re.match(r'^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$', orcid):
        raise ValueError('Invalid orcid should match xxxx-yyyy-zzzz-wwww: ' + orcid)
    digits = orcid.replace('-', '')[:15]
    total = 0
    for c in digits:
        total = ((total + int(c)) * 2) % 11
    result = (12 - total) % 11
    if result == 10:
        checksum = 'X'
    else:
        checksum = chr(result+48)
    if checksum != orcid[-1]:
        raise ValueError('Invalid orcid checksum: ' + orcid)

def parse_meta(metastr):
    """Read the meta file line by line. When we encounter author: or affiliation: or title: or
       funding: we know how to process subsequent lines that start with two spaces.
    args:
       metastr: UTF-8 string from a .meta file.
    Returns:
        a dict with fields for a Meta object.
    # TODO: define a JSON schema for this file, or return a pydantic object.
    """
    decoder = get_decoder()
    data = {'authors': [],
            'affiliations': [],
            'funders': []}

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
                if k == 'surname':
                    author['familyName'] = v
                elif k == 'name':
                    author[k] = v
                    v = decoder.latex_to_text(v)
                    parsed = HumanName(v)
                    if parsed:
                        author[k] = str(parsed) # canonicalize name
                        if parsed.last:
                            author['familyName'] = parsed.last
                        if parsed.first:
                            author['given'] = parsed.first
                    else: # surname is required, so guess if the parser fails.
                        parts = author[k].split()
                        author['familyName'] = parts[-1]
                elif k == 'email':
                    author['email'] = v.strip()
                    # This is just a basic check - not a full validation.
                    if not re.match(r'[^@]+@[^@]+\.[^@]+', author['email']):
                        raise valueError('Invalid email: ' + author['email'])
                elif k == 'affil' or k == 'inst':
                    author['affiliations'] = [a.strip() for a in v.split(',') if a.strip()]
                    for i in author['affiliations']:
                        if not i.isdigit():
                            raise ValueError('Invalid list of affiliations {}'.format(v))
                elif k == 'orcid':
                    author['orcid'] = v.rstrip()
                    validate_orcid(author['orcid'])
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
        elif line.startswith('schema:'):
            data['schema'] = line[7:].strip()
            index += 1
        elif line.startswith('title:'):
            data['title'] = decoder.latex_to_text(line[6:].strip())
            index += 1
            if index < numlines and lines[index].startswith('  '):
                k,v = get_key_val(lines[index])
                if k == 'subtitle':
                    data['subtitle'] = decoder.latex_to_text(v)
                    index += 1
        # metacapture writes out subtitle by itself. May occur before title:
        elif line.startswith('subtitle:'):
            data['subtitle'] = decoder.latex_to_text(line[9:].strip())
            index += 1
        elif line.startswith('keywords:'):
            data['keywords'] = [k.strip() for k in decoder.latex_to_text(line[9:].strip()).split(',')]
            index += 1
        elif line.startswith('license:'):
            data['license'] = line[8:].strip()
            index += 1
        else:
            raise Exception('unexpected line {}'.format(line))
    # perform a sanity check on affiliations to make sure the indices are in range.
    num_affiliations = len(data.get('affiliations'))
    for author in data.get('authors'):
        for aff in author.get('affiliations'):
            index = int(aff)
            if index not in range(1, 1+num_affiliations):
                raise ValueError('Author affiliations out of range for author {}'.format(author.get('name', '')))
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
