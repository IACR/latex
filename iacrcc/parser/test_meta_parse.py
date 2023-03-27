import pytest
from pylatexenc.latex2text import LatexNodes2Text
from .meta_parse import remove_macros

def test_cleaning():
    decoder = LatexNodes2Text(math_mode='with-delimiters', keep_braced_groups=False)
    cases = {r'This has \"umlaut': 'This has ümlaut',
             r'The title \thanks  {this works}': 'The title',
             r'This is\\ a long title': 'This is a long title',
             r'This has the last\index  {foo} part': 'This has the last part',
             r'We have \r a and \protect \$ for a dollar': 'We have å and $ for a dollar'

             }
    for input, output in cases.items():
        print(decoder.latex_to_text(input))
        assert decoder.latex_to_text(remove_macros(input)) == output
