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
            if ending in ['aux', 'out', 'bbl', 'pdf', 'blg', 'log', 'fls', 'fdb_latexmk', 'sty', 'xmpdata', 'meta']:
                f.unlink()
        try:
            os.chdir(tmpdir)
            proc = subprocess.run(['latexmk', '-g', eng, 'main'], capture_output=True)
            data = {'proc': proc}
            metafile = Path('main.meta')
            if metafile.is_file():
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
    # should fail with pdflatex.
    res = run_engine('-pdf', path.iterdir())
    assert res['proc'].returncode != 0

def test2_test():
    path = Path('test2')
    # should pass with lualatex.
    res = run_engine('-pdflua', path.iterdir())
    assert res['proc'].returncode == 0
    # should pass with pdflatex.
    res = run_engine('-pdf', path.iterdir())
    assert res['proc'].returncode != 0
            
def test3_test():
    path = Path('test3')
    # should pass with lualatex.
    res = run_engine('-pdflua', path.iterdir())
    assert res['proc'].returncode == 0
    # should pass with pdflatex.
    res = run_engine('-pdf', path.iterdir())
    assert res['proc'].returncode != 0
            
