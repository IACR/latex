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
            proc = subprocess.run(['latexmk', '-g', eng, 'main'], capture_output=True)
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
    assert meta['title'] == "Thoughts about \"binary\" functions on $GF(p)$ by Fester Bestertester\\ at 30\u00b0C"
    assert len(meta['authors']) == 3
    assert meta['authors'][0]['orcid'] == '0000-0003-1010-8157'
    assert meta['authors'][0]['affiliations'] == ['1','2']
    assert meta['authors'][1]['email'] == 'bad@example.com'
    assert meta['authors'][2]['name'] == 'Tancrède Lepoint'
    assert meta['affiliations'][0]['ror'] == '02t274463'
    assert meta['affiliations'][2]['name'] == 'Boğaziçi University'
    assert meta['affiliations'][2]['country'] == 'Turkey'
    assert meta['version'] == 'final'
    # should fail with pdflatex.
    res = run_engine('-pdf', path.iterdir())
    assert res['proc'].returncode != 0

def test2_test():
    path = Path('test2')
    # should pass with lualatex.
    res = run_engine('-pdflua', path.iterdir())
    assert res['proc'].returncode == 0
    meta = meta_parse.parse_meta(res['meta'])
    assert meta['title'] == 'How to Use the IACR Communications in Cryptology Class'
    assert meta['subtitle'] == 'A Template'
    assert meta['authors'][0]['name'] == 'Joppe W. Bos'
    assert meta['authors'][0]['email'] == 'joppe.bos@nxp.com'
    assert meta['authors'][0]['orcid'] == '0000-0003-1010-8157'
    assert meta['authors'][0]['affiliations'] == ['1']
    assert meta['authors'][1]['name'] == 'Kevin S. McCurley'
    assert meta['authors'][1]['email'] == 'test2@digicrime.com'
    assert meta['authors'][1]['orcid'] == '0000-0001-7890-5430'
    assert meta['authors'][1]['affiliations'] == ['2']
    affil = meta['affiliations'][0]
    assert affil['name'] == 'NXP Semïcönductors'
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
    # should pass with pdflatex.
    res = run_engine('-pdf', path.iterdir())
    assert res['proc'].returncode == 0

def test3_test():
    path = Path('test3')
    # should pass with lualatex.
    res = run_engine('-pdflua', path.iterdir())
    assert res['proc'].returncode == 0
    # should pass with pdflatex.
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
