import glob
import json
import os
from pathlib import Path
import pdfplumber
import pytest
import tempfile
import shutil
import subprocess
import sys
from xmp import XMPParser
sys.path.insert(0, '../')
from parser import meta_parse

def run_engine(eng, filelist, tmpdirpath):
    cwd = os.getcwd()
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
        proc = subprocess.run(['latexmk', '-f', '-interaction=nonstopmode', '-g', eng, 'main'], capture_output=True)
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
    with tempfile.TemporaryDirectory() as tmpdirpath:
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0
        assert 'meta' in res
        meta = meta_parse.parse_meta(res['meta'])
        assert meta['title'] == "Thoughts about \"binary\" functions and $ on $GF(p)$ by Fester Bestertester at 30\u00b0C"
        assert len(meta['authors']) == 3
        assert meta['authors'][0]['orcid'] == '0000-0003-1010-8157'
        assert meta['authors'][0]['affiliations'] == ['1','2']
        assert meta['authors'][1]['email'] == 'bad@example.com'
        assert meta['authors'][2]['name'] == 'Tancrède Lepoint'
        assert meta['affiliations'][0]['ror'] == '02t274463'
        assert meta['affiliations'][2]['name'] == 'Boğaziçi University'
        assert meta['affiliations'][2]['country'] == 'Turkey'
        assert meta['version'] == 'final'
    with tempfile.TemporaryDirectory() as tmpdirpath:
        # should fail with pdflatex because it has version=final.
        res = run_engine('-pdf', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode != 0

def test2_test():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test2')
        # should pass with lualatex.
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
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
        assert meta['keywords'][0] == 'Témplate'
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
    with tempfile.TemporaryDirectory() as tmpdirpath:
        res = run_engine('-pdf', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0

def test3_test():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test3')
        # should pass with lualatex.
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0
        meta = meta_parse.parse_meta(res['meta'])
        assert len(meta['citations']) == 79
        citation = meta['citations'][1]
        assert citation['title'] == 'Effect of immobilization on catalytic characteristics of saturated {Pd-N}-heterocyclic carbenes in {Mizoroki-Heck} reactions'
        assert len(citation['authorlist']) == 7
        authorlist = citation['authorlist']
        assert authorlist[0]['name'] == 'Özge Aksın'
    with tempfile.TemporaryDirectory() as tmpdirpath:
        # should fail to compile with pdflatex since it has version=final.
        res = run_engine('-pdf', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode != 0

# Negative test.
# Test a final version without an e-mail address provided
# --> This should fail.
def test4_test():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test4')
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode != 0

# Negative test.
# Test a final version without a license provided
# --> This should fail.
def test5_test():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test5')
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
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
    # with inputenc, fontenc and pdflatex, we get mixed encodings.
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

def test11_test():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test11')
        # should pass with lualatex.
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0
        meta = meta_parse.parse_meta(res['meta'])
        assert meta['title'] == 'How not to use the IACR Communications in Cryptology Cláss'
        print(json.dumps(meta,indent=2))
        assert len(meta['keywords']) == 2
        assert meta['keywords'][0] == 'Dirac delta function'
        assert meta['keywords'][1] == 'unit impulse'
        assert len(meta['funders']) == 3
        assert meta['funders'][0]['name'] == 'Horizon 2020 Framework Programme'
        assert meta['funders'][0]['grantid'] == '5211-2'
        assert meta['funders'][0]['fundref'] == '1241171'
        assert meta['funders'][0]['country'] == 'Elbonia'
        assert meta['funders'][1]['name'] == 'Just another foundation'
        assert meta['funders'][1]['ror'] == '042c84f31'
        assert meta['funders'][1]['country'] == 'United States'
        assert meta['funders'][2]['name'] == 'National Fantasy Foundation'
        assert meta['funders'][2]['fundref'] == '517622'
        assert meta['funders'][2]['grantid'] == '57821-3'
        assert 'country' not in meta['funders'][2]
        pdfpath = tmpdirpath + '/main.pdf'
        xmp = XMPParser(pdfpath)
        description = xmp.get_string('.//dc:description/rdf:Alt/rdf:li')
        assert description == 'IACR Communications in Cryptology, DOI:XXXXXXXX'
        assert xmp.get_string('.//dc:identifier') == 'info:doi/XXXXXXXX'
        assert xmp.get_string('.//prism:publicationName') == 'IACR Communications in Cryptology'
        assert xmp.get_string('.//prism:doi') == 'XXXXXXXX'
        assert xmp.get_string('.//prism:publicationName') == 'IACR Communications in Cryptology'
        assert xmp.get_string('.//prism:aggregationType') == 'journal'
        assert xmp.get_string('.//dc:source') == 'main.tex'


def test12_test():
    # Check for presence of author name with notanonymous.
    # also check XMP data.
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test12')
        # should pass with lualatex.
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0
        meta = meta_parse.parse_meta(res['meta'])
        assert meta['title'] == 'An example that is not anonymous'
        pdfpath = tmpdirpath + '/main.pdf'
        xmp = XMPParser(pdfpath)
        title = xmp.get_string('.//dc:title/rdf:Alt/rdf:li')
        assert title == 'An example that is not anonymous'
        authors = xmp.get_strings('.//dc:creator/rdf:Seq/rdf:li')
        assert len(authors) == 2
        assert authors[0] == 'Joppe W. Bös'
        assert authors[1] == 'Kevin S. McCurley'
        description = xmp.get_string('.//dc:description/rdf:Alt/rdf:li')
        assert description is None
        marked = xmp.get_string('.//xmpRights:Marked')
        assert marked == 'True'
        webStatement = xmp.get_string('.//xmpRights:WebStatement')
        assert webStatement == 'https://creativecommons.org/licenses/by/4.0/deed.en'
        rights = xmp.get_string('.//dc:rights/rdf:Alt/rdf:li')
        assert rights == 'This work is licensed under a Creative Commons "Attribution 4.0 International" license.'
        byteCount = xmp.get_string('.//prism:byteCount')
        assert int(byteCount) > 40000
        pageCount = xmp.get_string('.//prism:pageCount')
        assert int(pageCount) == 1
        source = xmp.get_string('.//dc:source')
        assert source == 'main.tex'
        keywords = xmp.get_string('.//pdf:Keywords')
        assert keywords == 'stuff, other random'
        subject = xmp.get_strings('.//dc:subject/rdf:Bag/rdf:li')
        assert len(subject) == 2
        assert subject[0] == 'stuff'
        assert subject[1] == 'other random'
        identifier = xmp.get_string('.//dc:identifier')
        assert identifier is None
        doi = xmp.get_string('.//prism:doi')
        assert doi is None
        pubname = xmp.get_string('.//prism:publicationName')
        assert pubname is None
        aggregation = xmp.get_string('.//prism:aggregationType')
        assert aggregation is None

        # Make sure author names appear in the paper with notanonymous
        with pdfplumber.open(pdfpath) as pdf:
            first_page = pdf.pages[0].extract_text()
            assert 'Kevin S. McCurley' in first_page
            assert 'Joppe W. Bös' in first_page

def test13_test():
    # Check for absence of author name with submission without notanonymous
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test13')
        # should pass with lualatex.
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0
        meta = meta_parse.parse_meta(res['meta'])
        assert meta['title'] == 'An example that is not anonymous'
        pdfpath = tmpdirpath + '/main.pdf'
        xmp = XMPParser(pdfpath)
        assert xmp.get_string('.//dc:title/rdf:Alt/rdf:li') == 'An example that is not anonymous'
        assert xmp.get_string('.//dc:creator/rdf:Seq/rdf:li') == 'hidden for submission'
        assert xmp.get_string('.//pdf:Keywords') == 'stuff, other random'
        subject = xmp.get_strings('.//dc:subject/rdf:Bag/rdf:li')
        assert subject[0] == 'stuff'
        assert subject[1] == 'other random'
        assert xmp.get_string('.//dc:source') == 'main.tex'
        assert xmp.get_string('.//xmpTPg:NPages') == str(1)
        # Make sure author names appear in the paper with notanonymous
        with pdfplumber.open(pdfpath) as pdf:
            first_page = pdf.pages[0].extract_text()
            assert 'Kevin S. McCurley' not in first_page
            assert 'Joppe W. Bös' not in first_page


def test14_test():
    # Check for line numbers in copyedit version
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test14')
        # should pass with lualatex.
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0
        logpath = tmpdirpath + '/main.log'
        log = Path(logpath).read_text(encoding='UTF-8')
        assert 'lineno.sty' in log
        pdfpath = tmpdirpath + '/main.pdf'
        with pdfplumber.open(pdfpath) as pdf:
            text = pdf.pages[1].extract_text()
            print(text)
            assert '39' in text
            assert '78' in text

# Negative test.
# Check if we detect a newline using "\newline" in the addauthor command
# --> This should fail.
def test15_test():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test15')
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode != 0

# Test a submission with 30 authors all with footnotes
def test16_test():
    path = Path('test16')
    # should pass with lualatex.
    with tempfile.TemporaryDirectory() as tmpdirpath:
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0
    # should pass with pdflatex
    with tempfile.TemporaryDirectory() as tmpdirpath:
        res = run_engine('-pdf', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0

# Negative test.
# Check if we detect a newline using "\\" in the addauthor command
# --> This should fail.
def test17_test():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test17')
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode != 0

# Negative test.
# Check if we detect using a " and " in the addauthor command
# --> This should fail.
def test18_test():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test18')
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode != 0

# Negative test.
# Check if we detect using a " \and " in the addauthor command
# --> This should fail.
def test19_test():
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test19')
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode != 0

def test20_test():
    # Check if a paper with one author and two affiliations 
    # does *not* show the institure markers
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test20')
        # should pass with lualatex.
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0
        pdfpath = tmpdirpath + '/main.pdf'
        with pdfplumber.open(pdfpath) as pdf:
            text = pdf.pages[0].extract_text()
            print(text)
            assert 'Freddy First1' not in text
            assert 'Freddy First 1' not in text
            assert '1Company' not in text
            assert '1 Company' not in text
            assert '2University' not in text
            assert '2 University' not in text
            
def test21_test():
    # Check that we need \runningauthors
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test21')
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode != 0

def test22_test():
    # Check that it compiles with \runningauthors
    with tempfile.TemporaryDirectory() as tmpdirpath:
        path = Path('test22')
        res = run_engine('-pdflua', path.iterdir(), tmpdirpath)
        assert res['proc'].returncode == 0
        meta = meta_parse.parse_meta(res['meta'])
        assert meta['title'] == 'How not to use the IACR Communic̄ations in Cryptology Class'
