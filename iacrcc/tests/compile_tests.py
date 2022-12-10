import glob
import json
import os
from pathlib import Path
import pytest
import tempfile
import shutil
import subprocess
import sys
sys.path.insert(0, '../')
from parser import meta_parse

def run_engine(eng, filelist):
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdirpath:
        for f in filelist:
            if f.is_file():
                shutil.copy(f, tmpdirpath)
        # remove any temporary files
        tmpdir = Path(tmpdirpath)
        for f in tmpdir.iterdir():
            ending = str(f).split('.')[-1]
            if ending in ['abstract', 'aux', 'out', 'bbl', 'pdf', 'blg', 'log', 'fls', 'fdb_latexmk', 'sty', 'xmpdata', 'meta', 'bcf', 'xml']:
                f.unlink()
        try:
            os.chdir(tmpdir)
            proc = subprocess.run(['latexmk', '-f', '-interaction=nonstopmode' '-g', eng, 'main'], capture_output=True)
            data = {'proc': proc}
            metafile = Path('main.meta')
            if metafile.is_file() and eng == '-pdflua':
                data['meta'] = metafile.read_text(encoding='UTF-8')
            return data
        finally:
            os.chdir(cwd)

def test1_test():
    path = Path('test1')
    # should pass with lualatex.
    res = run_engine('-pdflua', path.iterdir())
    assert res['proc'].returncode == 0
    assert 'meta' in res
    meta = meta_parse.parse_meta(res['meta'])
    assert meta['title'] == "Thoughts about \"binary\" functions on $GF(p)$ by Fester Bestertester at 30\u00b0C"
    assert len(meta['authors']) == 3
    assert meta['authors'][0]['orcid'] == '0000-0003-1010-8157'
    assert meta['authors'][0]['affiliations'] == ['1','2']
    assert meta['authors'][1]['email'] == 'bad@example.com'
    assert meta['authors'][2]['name'] == 'Tancrède Lepoint'
    assert meta['affiliations'][0]['ror'] == '02t274463'
    assert meta['affiliations'][2]['name'] == 'Boğaziçi University'
    assert meta['affiliations'][2]['country'] == 'Turkey'
    assert meta['version'] == 'final'
    # should fail with pdflatex because it has version=final.
    res = run_engine('-pdf', path.iterdir())
    assert res['proc'].returncode != 0

def test2_test():
    path = Path('test2')
    # should pass with lualatex.
    res = run_engine('-pdflua', path.iterdir())
    assert res['proc'].returncode == 0
    meta = meta_parse.parse_meta(res['meta'])
    assert meta['title'] == 'How to Use the IACR Communications in Cryptology Clåss'
    assert meta['subtitle'] == 'A Template'
    assert meta['authors'][0]['name'] == 'Joppe W. Bös'
    assert meta['authors'][0]['email'] == 'joppe.bos@nxp.com'
    assert meta['authors'][0]['orcid'] == '0000-0003-1010-8157'
    assert meta['authors'][0]['affiliations'] == ['1']
    assert meta['authors'][1]['name'] == 'Kevin S. McCurley'
    assert meta['authors'][1]['email'] == 'test2@digicrime.com'
    assert meta['authors'][1]['orcid'] == '0000-0001-7890-5430'
    assert meta['authors'][1]['affiliations'] == ['2']
    affil = meta['affiliations'][0]
    assert affil['name'] == 'NXP Sěmïcöndúctørs'
    assert affil['ror'] == '031v4g827'
    assert affil['street'] == 'Interleuvenlaan 80'
    assert affil['city'] == 'Leuven'
    assert affil['postcode'] == '3001'
    assert affil['country'] == 'Belgium'
    assert len(meta['keywords']) == 3
    assert meta['keywords'][0] == 'Template'
    assert meta['keywords'][1] == 'LaTeX'
    assert meta['keywords'][2] == 'IACR'
    assert meta['version'] == 'preprint'
    assert len(meta['citations']) == 6
    citation = meta['citations'][0]
    assert citation['id'] == 'fancynames'
    assert citation['title'] == 'Something about mathematics $x^n+y^n=z^n$ when $n=2$'
    assert len(citation['authorlist']) == 6
    assert citation['authorlist'][0]['name'] == 'Jeroen von Bücher'
    assert citation['authorlist'][0]['surname'] == 'von Bücher'
    assert citation['authorlist'][2]['name'] == 'Öznur Küçükkubaş'
    citation = meta['citations'][3]['doi'] == '10.1007/3-540-68697-5_9'
    # should at least compile with pdflatex.
    res = run_engine('-pdf', path.iterdir())
    assert res['proc'].returncode == 0

def test3_test():
    path = Path('test3')
    # should pass with lualatex.
    res = run_engine('-pdflua', path.iterdir())
    assert res['proc'].returncode == 0
    meta = meta_parse.parse_meta(res['meta'])
    assert len(meta['citations']) == 79
    citation = meta['citations'][1]
    assert citation['title'] == 'Effect of immobilization on catalytic characteristics of saturated {Pd-N}-heterocyclic carbenes in {Mizoroki-Heck} reactions'
    assert len(citation['authorlist']) == 7
    authorlist = citation['authorlist']
    assert authorlist[0]['name'] == 'Özge Aksın'
    # should fail to compile with pdflatex since it has version=final.
    res = run_engine('-pdf', path.iterdir())
    assert res['proc'].returncode != 0

# Negative test.
# Test a final version without an e-mail address provided
# --> This should fail.
def test4_test():
    path = Path('test4')
    res = run_engine('-pdflua', path.iterdir())
    assert res['proc'].returncode != 0

# Negative test.
# Test a final version without a license provided
# --> This should fail.
def test5_test():
    path = Path('test5')
    res = run_engine('-pdflua', path.iterdir())
    assert res['proc'].returncode != 0

# This is used for test6 in which we generate an output file main.output
# using with \write under different conditions. We don't try to parse this
# as metadata, and main.meta will not be created.
def get_output(eng, main_file):
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdirpath:
        shutil.copy(main_file, tmpdirpath)
        tmpdir = Path(tmpdirpath)
        try:
            os.chdir(tmpdir)
            proc = subprocess.run(['latexmk', '-f', '-interaction=nonstopmode' '-g', eng, 'main'], capture_output=True)
            data = {'proc': proc}
            data['log'] = Path('main.log').read_text(encoding='UTF-8')
            outputfile = Path('main.output')
            if outputfile.is_file():
                try:
                    data['bytes'] = outputfile.read_bytes()
                except Exception as e:
                    data['error'] = str(e)
            return data
        except Exception as e:
            return {'error': str(e)}
        finally:
            os.chdir(cwd)

def test6_test():
    """no fontenc and no fontspec."""
    res = get_output('-pdflua', Path('test6/main.tex'))
    assert res['proc'].returncode == 0
    output = res['bytes'].decode('utf-8', 'strict').splitlines()
    assert len(output) == 9
    assert output[0] == 'Insertstuff.'
    assert output[1] == 'With space:Insert\\ stuff.'
    assert output[2] == 'With braces:Insert{} stuff.'
    assert output[3] == 'With tilde: Insert\\protect \\unhbox \\voidb@x \\protect \\penalty \\@M \\ {}stuff.'
    assert output[4] == 'accented: å ü \\TU\\DJ '
    assert output[5] == 'With math $\\alpha $'
    assert output[6] == 'Puret:Āā Ēē Īī Ōō Ūū Ȳȳ ü alpha with $a=b$'
    assert output[7] == 'å and Š ü \\TU\\i \\TU\\DJ '
    assert output[8] == 'Puret:å and Š ü ıĐ'

def test7_test():
    # with fontenc and pdflatex, we get malformed output.
    res = get_output('-pdf', Path('test7/main.tex'))
    assert res['proc'].returncode == 0
    # The output file is not UTF-8
    with pytest.raises(Exception):
        res['bytes'].decode('utf-8', 'strict')
    output = res['bytes'].decode('iso_8859_1').splitlines()
    assert len(output) == 9
    assert output[0] == 'Insertstuff.'
    assert output[1] == 'With space:Insert\\ stuff.'
    assert output[2] == 'With braces:Insert{} stuff.'
    assert output[3] == 'With tilde: Insert\\protect \\unhbox \\voidb@x \\protect \\penalty \\@M \\ {}stuff.'
    assert output[4] == 'accented: å ü \\T1\\DJ ' # note encoding
    assert output[5] == 'With math $\\alpha $'
    print(output[6])
    assert output[6] == 'Puret:Ä\x80Ä\x81 Ä\x92Ä\x93 ÄªÄ« Å\x8cÅ\x8d ÅªÅ« È²È³ Ã¼ alpha with $a=b$'
    assert output[7] == 'å and Å  ü \\T1\\i \\T1\\DJ ' # note bad encoding
    b = ':'.join(hex(ord(char)) for char in output[8][:15])
    assert b == '0x50:0x75:0x72:0x65:0x74:0x3a:0xc3:0xa5:0x20:0x61:0x6e:0x64:0x20:0xc5:0xa0'
    #              P   u    r    e    t    :    Ã     ¥   sp   a    n    d    sp   Å    nbsp
    assert output[8][:15] == 'Puret:Ã¥ and Å\xa0'
    assert hex(ord(output[8][-1])) == '0x90' # control character at the end.

def test8_test():
    """fontenc and lualatex will at least not be bad encoding."""
    res = get_output('-pdflua', Path('test8/main.tex'))
    assert res['proc'].returncode == 0
    output = res['bytes'].decode('utf-8', 'strict').splitlines()
    assert len(output) == 9
    assert output[0] == 'Insertstuff.'
    assert output[1] == 'With space:Insert\\ stuff.'
    assert output[2] == 'With braces:Insert{} stuff.'
    assert output[3] == 'With tilde: Insert\\protect \\unhbox \\voidb@x \\protect \\penalty \\@M \\ {}stuff.'
    assert output[4] == 'accented: å ü \\TU\\DJ ' # note encoding
    assert output[5] == 'With math $\\alpha $' # extra space in math after macro \alpha
    assert output[6] == 'Puret:Āā Ēē Īī Ōō Ūū Ȳȳ ü alpha with $a=b$' # gobble space after Pure
    assert output[7] == 'å and Š ü \\TU\\i \\TU\\DJ ' # T1 encoding
    assert output[8] == 'Puret:å and Š ü ıĐ'

def test9_test():
    """fontspec and lualatex will at least not be bad encoding."""
    res = get_output('-pdflua', Path('test9/main.tex'))
    assert res['proc'].returncode == 0
    output = res['bytes'].decode('utf-8', 'strict').splitlines()
    assert len(output) == 10
    assert output[0] == 'Insertstuff.'
    assert output[1] == 'With space:Insert\\ stuff.'
    assert output[2] == 'With braces:Insert{} stuff.'
    assert output[3] == 'With tilde: Insert\\protect \\unhbox \\voidb@x \\protect \\penalty \\@M \\ {}stuff.'
    assert output[4] == 'accented: å ü \\TU\\DJ ' # note encoding
    assert output[5] == 'With math $\\alpha $' # extra space in math after macro \alpha
    assert output[6] == 'Puret:Āā Ēē Īī Ōō Ūū Ȳȳ ü alpha with $a=b$' # gobble space after Pure
    assert output[7] == 'å and Š ü \\TU\\i \\TU\\DJ ' # T1 encoding
    assert output[8] == 'Puret:å and Š ü ıĐ'
    # MISSING CHARACTERS IN PDF!
    assert 'Missing character: There is no Ȳ (U+0232) in font [lmroman10-regular]:+tlig;!' in res['log']
    assert 'Missing character: There is no ȳ' in res['log']
    assert output[9] == 'Unicode math $ȳ=Ē$'
    # FAILS with pdflatex
    res = get_output('-pdf', Path('test9/main.tex'))
    assert res['proc'].returncode != 0

def test10_test():
    """test of \tracinglostchars=3 to catch something not defined."""
    res = get_output('-pdflua', Path('test10/main.tex'))
    assert res['proc'].returncode != 0
    res = get_output('-pdf', Path('test10/main.tex'))
    assert res['proc'].returncode != 0
