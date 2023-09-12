import glob
import json
import os
from pathlib import Path
import pdfplumber
import pytest
import re
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
    else:
      print(str(f))
  try:
    os.chdir(tmpdir)
    proc = subprocess.run(['latexmk', '-f', '-interaction=nonstopmode', '-g', eng, 'main'], capture_output=True)
    data = {'proc': proc}
    metafile = Path('main.meta')
    if metafile.is_file():# and eng == '-pdflua':
      data['meta'] = metafile.read_text(encoding='UTF-8')
    logfile = Path('main.log')
    if logfile.is_file():
      data['log'] = logfile.read_text('utf-8', errors='replace')
    return data
  finally:
    os.chdir(cwd)

def test1_test():
  path = Path('test1')
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      res = run_engine(option, path.iterdir(), tmpdirpath)
      print(res)
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
    
def test2_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test2')
      res = run_engine(option, path.iterdir(), tmpdirpath)
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

def test3_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test3')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode == 0
      meta = meta_parse.parse_meta(res['meta'])

# Negative test.
# Test a final version without an e-mail address provided
# --> This should fail.
def test4_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test4')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode != 0

# Negative test.
# Test a final version without a license provided
# --> This should fail.
def test5_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test5')
      res = run_engine(option, path.iterdir(), tmpdirpath)
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

# TODO: Fix or adjust test7
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
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test11')
      res = run_engine(option, path.iterdir(), tmpdirpath)
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
      #pdfpath = tmpdirpath + '/main.pdf'
      #xmp = XMPParser(pdfpath)
      #description = xmp.get_string('.//dc:description/rdf:Alt/rdf:li')
      #assert description == 'IACR Communications in Cryptology, DOI:XXXXXXXX'
      #assert xmp.get_string('.//dc:identifier') == 'info:doi/XXXXXXXX'
      #assert xmp.get_string('.//prism:publicationName') == 'IACR Communications in Cryptology'
      #assert xmp.get_string('.//prism:doi') == 'XXXXXXXX'
      #assert xmp.get_string('.//prism:publicationName') == 'IACR Communications in Cryptology'
      #assert xmp.get_string('.//prism:aggregationType') == 'journal'
      #assert xmp.get_string('.//dc:source') == 'main.tex'
      #authors = xmp.get_strings('.//dc:creator/rdf:Seq/rdf:li')
      #assert len(authors) == 2

# TODO: Test12 fails with pdflatex
# The problem seems to be in:
#      byteCount = xmp.get_string('.//prism:byteCount')
#      assert int(byteCount) > 40000
def test12_test():
  # Check for presence of author name with notanonymous.
  # also check XMP data.
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test12')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode == 0
      meta = meta_parse.parse_meta(res['meta'])
      assert meta['title'] == 'An example that is not anonymous'
      pdfpath = tmpdirpath + '/main.pdf'
      #xmp = XMPParser(pdfpath)
      #title = xmp.get_string('.//dc:title/rdf:Alt/rdf:li')
      #assert title == 'An example that is not anonymous'
      #authors = xmp.get_strings('.//dc:creator/rdf:Seq/rdf:li')
      #assert len(authors) == 2
      #assert authors[0] == 'Joppe W. Bös'
      #assert authors[1] == 'Kevin S. McCurley'
      #description = xmp.get_string('.//dc:description/rdf:Alt/rdf:li')
      #assert description is None
      #marked = xmp.get_string('.//xmpRights:Marked')
      #assert marked == 'True'
      #webStatement = xmp.get_string('.//xmpRights:WebStatement')
      #assert webStatement == 'https://creativecommons.org/licenses/by/4.0/deed.en'
      #rights = xmp.get_string('.//dc:rights/rdf:Alt/rdf:li')
      #assert rights == 'This work is licensed under a Creative Commons "Attribution 4.0 International" license.'
      #if option == 'pdflua':
      #  # this does not exist under pdflatex. See https://github.com/borisveytsman/acmart/issues/413
      #  byteCount = xmp.get_string('.//prism:byteCount')
      #  assert int(byteCount) > 40000
      #pageCount = xmp.get_string('.//prism:pageCount')
      #assert int(pageCount) == 1
      #source = xmp.get_string('.//dc:source')
      #assert source == 'main.tex'
      #keywords = xmp.get_string('.//pdf:Keywords')
      #assert keywords == 'stuff, other random'
      #subject = xmp.get_strings('.//dc:subject/rdf:Bag/rdf:li')
      #assert len(subject) == 2
      #assert subject[0] == 'stuff'
      #assert subject[1] == 'other random'
      #identifier = xmp.get_string('.//dc:identifier')
      #assert identifier is None
      #doi = xmp.get_string('.//prism:doi')
      #assert doi is None
      #pubname = xmp.get_string('.//prism:publicationName')
      #assert pubname is None
      #aggregation = xmp.get_string('.//prism:aggregationType')
      #assert aggregation is None

      # Make sure author names appear in the paper with notanonymous
      with pdfplumber.open(pdfpath) as pdf:
        first_page = pdf.pages[0].extract_text()
        assert 'Kevin S. McCurley' in first_page
        assert 'Joppe W. Bös' in first_page

def test13_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    # Check for absence of author name with submission without notanonymous
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test13')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode == 0
      meta = meta_parse.parse_meta(res['meta'])
      assert meta['title'] == 'An example that is not anonymous'
      pdfpath = tmpdirpath + '/main.pdf'
      #xmp = XMPParser(pdfpath)
      #assert xmp.get_string('.//dc:title/rdf:Alt/rdf:li') == 'An example that is not anonymous'
      #assert xmp.get_string('.//dc:creator/rdf:Seq/rdf:li') == 'hidden for submission'
      #assert xmp.get_string('.//pdf:Keywords') == 'stuff, other random'
      #assert xmp.get_string('.//dc:source') == 'main.tex'
      #assert xmp.get_string('.//xmpTPg:NPages') == str(1)
      # Make sure author names appear in the paper with notanonymous
      with pdfplumber.open(pdfpath) as pdf:
        first_page = pdf.pages[0].extract_text()
        assert 'Kevin S. McCurley' not in first_page
        assert 'Joppe W. Bös' not in first_page

def test14_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    # Check for line numbers in copyedit version
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test14')
      res = run_engine(option, path.iterdir(), tmpdirpath)
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
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test15')
      res = run_engine('option', path.iterdir(), tmpdirpath)
      assert res['proc'].returncode != 0

# Test a submission with 30 authors all with footnotes
def test16_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    path = Path('test16')
    with tempfile.TemporaryDirectory() as tmpdirpath:
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode == 0

# Negative test.
# Check if we detect a newline using "\\" in the addauthor command
# --> This should fail.
def test17_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test17')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode != 0

# Negative test.
# Check if we detect using a " and " in the addauthor command
# --> This should fail.
def test18_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test18')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode != 0

# Negative test.
# Check if we detect using a " \and " in the addauthor command
# --> This should fail.
def test19_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test19')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode != 0

def test20_test():
  # Check if a paper with one author and two affiliations 
  # does *not* show the institure markers
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test20')
      res = run_engine(option, path.iterdir(), tmpdirpath)
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
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test21')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode != 0

def test22_test():
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    # Check that it compiles with \runningauthors
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test22')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode == 0
      meta = meta_parse.parse_meta(res['meta'])
      assert meta['title'] == 'How not to use the IACR Communic̄ations in Cryptology Class'

def test23_test():
  # Try to \@writemeta on a bunch of titles from eprint.
  for option in ['-pdflua', '-pdf']:
    # Check that it compiles with \runningauthors
    with tempfile.TemporaryDirectory() as tmpdirpath:
      path = Path('test23')
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode == 0
      line = res['meta'].splitlines()
      print(line[0])
      assert line[0] == r"title: On the possibility of basing Cryptography on the assumption that $P \protect \neq  NP$"
      assert line[1] == r"title: Black-Box Concurrent Zero-Knowledge Requires $\protect \tilde  \Omega (\log n)$ Rounds"
      assert line[2] == r"title: Parallel scalar multiplication on general elliptic curves over $\protect \mathbb  {F}_p$ hedged against Non-Differential Side-Channel Attacks"
      assert line[3] == r"title: An Upper Bound on the Size of a Code with the $k$-Identifiable Parent Property"
      assert line[4] == r"title: New covering radius of Reed-Muller codes for $t$-resilient functions"
      assert line[5] == r"title: Counting Points for Hyperelliptic Curves of type $y^2=x^5+ax$ over Finite Prime Fields"
      assert line[6] == r"title: Goldbach’s Conjecture on ECDSA Protocols"
      assert line[7] == r"title: Isomorphism Classes of Hyperelliptic Curves of Genus 2 over $\protect \mathbb  {F}_{2^n}$"
      assert line[8] == r"title: Point Compression on Jacobians of Hyperelliptic Curves over $F_q$."
      assert line[9] == r"title: Redundant Trinomials for Finite Fields of Characteristic $2$"
      assert line[10] == r"title: A Dynamic and Differential CMOS Logic Style to Resist Power and Timing Attacks on Security IC’s."
      assert line[11] == r"title: Charge Recycling Sense Amplifier Based Logic: Securing Low Power Security IC’s against Differential Power Analysis"
      assert line[12] == r"title: The Sorcerer’s Apprentice Guide to Fault Attacks"
      assert line[13] == r"title: Classification of genus 2 curves over $\protect \mathbb  {F}_{2^n}$ and optimization of their arithmetic"
      assert line[14] == r"title: Fast addition on non-hyperelliptic genus $3$ curves"
      assert line[15] == r"title: Suitable Curves for Genus-4 HCC over Prime Fields: Point Counting Formulae for Hyperelliptic Curves of type $y^2=x^{2k+1}+ax$"
      assert line[16] == r"title: Improvement of Thériault Algorithm of Index Calculus for Jacobian of Hyperelliptic Curves of Small Genus"
      assert line[17] == r"title: Covering Radius of the $(n-3)$-rd Order Reed-Muller Code in the Set of Resilient Functions"
      assert line[18] == r"title: DISTRIBUTION OF R-PATTERNS IN THE KERDOCK-CODE BINARY SEQUENCES AND THE HIGHEST LEVEL SEQUENCES OF PRIMITIVE SEQUENCES OVER $Z_{2^l}$"
      assert line[19] == r"title: Applications of $\protect \mathcal  {M}$ultivariate $\protect \mathcal  {Q}$uadratic Public Key Systems"
      assert line[20] == r"title: Parallel Montgomery Multiplication in $GF(2^k)$ using Trinomial Residue Arithmetic"
      assert line[21] == r"title: Cryptanalysis of Noel McCullagh and Paulo S. L. M. Barreto¡¯s two-party identity-based key agreement"
      assert line[22] == r"title: A note on López-Dahab coordinates"
      assert line[23] == r"title: Equivalent Keys in HFE, C$^*$, and variations"
      assert line[24] == r"title: A new security proof for Damgård's ElGamal"
      assert line[25] == r"title: A Metric on the Set of Elliptic Curves over ${\protect \mathbf  F}_p$."
      assert line[26] == r"title: Comment on cryptanalysis of Tseng et al.¡¦s authenticated encryption schemes"
      assert line[27] == r"title: BROADCAST ENCRYPTION $\pi $"
      assert line[28] == r"title: Finding MD5 Collisions – a Toy For a Notebook"
      assert line[29] == r"title: Cryptographer's Toolkit for Construction of $8$-Bit Bent Functions"
      assert line[30] == r"title: Almost Perfect Nonlinear Monomials over GF($2^n$) for Infinitely Many $n$"
      assert line[31] == r"title: A Uniform Framework for Cryptanalysis of the Bluetooth $E_0$ Cipher"
      assert line[32] == r"title: Secret sharing on the $d$-dimensional cube"
      assert line[33] == r"title: Minimality of the Hamming Weight of the \tau -NAF for Koblitz Curves and Improved Combination with Point Halving"
      assert line[34] == r"title: On the binary sequences with high $GF(2)$ linear complexities and low $GF(p)$ linear complexities"
      assert line[35] == r"title: Efficient reduction of 1 out of $n$ oblivious transfers in random oracle model"
      assert line[36] == r"title: Classification of Cubic $(n-4)$-resilient Boolean Functions"
      assert line[37] == r"title: Secure and {\protect \sl  Practical} Identity-Based Encryption"
      assert line[38] == r"title: Key Mixing in Block Ciphers through Addition modulo $2^n$"
      assert line[39] == r"title: Unified Point Addition Formulæ and Side-Channel Attacks"
      assert line[40] == r"title: Improvement of Manik et al.¡¦s remote user authentication scheme"
      assert line[41] == r"title: Weakness of shim¡¦s New ID-based tripartite multiple-key agreement protocol"
      assert line[42] == r"title: Gröbner Basis Based Cryptanalysis of SHA-1"
      assert line[43] == r"title: Tate pairing for $y^{2}=x^{5}-\alpha x$ in Characteristic Five"
      assert line[44] == r"title: Low Complexity Bit-Parallel Square Root Computation over GF($2^m$) for all Trinomials"
      assert line[45] == r"title: The Design Principle of Hash Function with Merkle-Damgård Construction"
      assert line[46] == r"title: Divisibility of the Hamming Weight by $2^k$ and Monomial Criteria for Boolean Functions"
      assert line[47] == r"title: There exist Boolean functions on $n$ (odd) variables having nonlinearity $> 2^{n-1} - 2^{\protect \frac  {n-1}{2}}$ if and only if $n > 7$"
      assert line[48] == r"title: Ate pairing for $y^{2}=x^{5}-\alpha x$ in characteristic five"
      assert line[49] == r"title: On (Hierarchical) Identity Based Encryption Protocols with Short Public Parameters \\ (With an Exposition of Waters' Artificial Abort Technique)"
      assert line[50] == r"title: An Algorithm for the $\eta _T$ Pairing Calculation in Characteristic Three and its Hardware Implementation"
      assert line[51] == r"title: RadioGatún, a belt-and-mill hash function"
      assert line[52] == r"title: Hardware Implementation of the $\eta _T$ Pairing in Characteristic 3"
      assert line[53] == r"title: Another class of quadratic APN binomials over $F_{2^n}$: the case $n$ divisible by 4"
      assert line[54] == r"title: Some Efficient Algorithms for the Final Exponentiation of $\eta _T$ Pairing"
      assert line[55] == r"title: How to Win the Clone Wars: \\ Efficient Periodic n-Times Anonymous Authentication"
      assert line[56] == r"title: Cryptanalysis of Hwang-Chang’s a Time-Stamp Protocol for Digital Watermarking"
      assert line[57] == r"title: A Coprocessor for the Final Exponentiation of the $\eta _T$ Pairing in Characteristic Three"
      assert line[58] == r"title: High Efficiency Feedback Shift Register: $\sigma -$LFSR"
      assert line[59] == r"title: Edon--${\protect \cal  R}(256,384,512)$ -- an Efficient Implementation of Edon--${\protect \cal  R}$ Family of Cryptographic Hash Functions"
      assert line[60] == r"title: The constructing of $3$-resilient Boolean functions of $9$ variables with nonlinearity $240$."
      assert line[61] == r"title: Voting with Unconditional Privacy by Merging Prêt-à-Voter and PunchScan"
      assert line[62] == r"title: A Refined Algorithm for the $\eta _T$ Pairing Calculation in Characteristic Three"
      assert line[63] == r"title: SECURITY PROOF FOR SHENGBAO WANG’S IDENTITY-BASED ENCRYPTION SCHEME"
      assert line[64] == r"title: On the Big Gap Between $|p|$ and $|q|$ in DSA"
      assert line[65] == r"title: Secure PRNGs from Specialized Polynomial Maps over Any $F_q$"
      assert line[66] == r"title: Algorithms and Arithmetic Operators for Computing the $\eta _T$ Pairing in Characteristic Three"
      assert line[67] == r"title: Computing the Ate Pairing on Elliptic Curves with Embedding Degree $k=9$"
      assert line[68] == r"title: Notes on the Wang et al. $2^{63}$ SHA-1 Differential Path"
      assert line[69] == r"title: A Proof of Security in $O(2^n)$ for the Xor of Two Random Permutations\\ -- Proof with the ``$H_{\sigma }$ technique''--"
      assert line[70] == r"title: Pairing-friendly Hyperelliptic Curves with Ordinary Jacobians of Type $y^2=x^5+ax$"
      assert line[71] == r"title: Merkle's Key Agreement Protocol is Optimal: An $O(n^2)$ Attack on any Key Agreement from Random Oracles"
      assert line[72] == r"title: A Comparison Between Hardware Accelerators for the Modified Tate Pairing over $\protect \mathbb  {F}_{2^m}$ and $\protect \mathbb  {F}_{3^m}$"
      assert line[73] == r"title: TinyECCK: Efficient Elliptic Curve Cryptography Implementation over $GF(2^m)$ on 8-bit MICAz Mote"
      assert line[74] == r"title: A Pipelined Karatsuba-Ofman Multiplier over GF($3^{97}$) Amenable for Pairing Computation"
      assert line[75] == r"title: Constant-Size Dynamic $k$-TAA"
      assert line[76] == r"title: Redundant $\tau $-adic Expansions I: Non-Adjacent Digit Sets and their Applications to Scalar Multiplication"
      assert line[77] == r"title: Redundant $\tau $-adic Expansions II: Non-Optimality and Chaotic Behaviour"
      assert line[78] == r"title: On The Security of The ElGamal Encryption Scheme and Damgard’s Variant"
      assert line[79] == r"title: Polynomials for Ate Pairing and $\protect \mathbf  {Ate}_{i}$ Pairing"
      assert line[80] == r"title: Remarks on the Attack of Fouque et al. against the {\ell }IC Scheme"
      assert line[81] == r"title: On the CCA1-Security of Elgamal and Damgård's Elgamal"
      assert line[82] == r"title: ON MIDDLE UNIVERSAL $m$-INVERSE QUASIGROUPS AND THEIR APPLICATIONS TO CRYPTOGRAPHY"
      assert line[83] == r"title: FPGA and ASIC Implementations of the $\eta _T$ Pairing in Characteristic Three"
      assert line[84] == r"title: Foundations of Group Key Management – Framework, Security Model and a Generic Construction"
      assert line[85] == r"title: A New $(k,n)$-Threshold Secret Sharing Scheme and Its Extension"
      assert line[86] == r"title: Generalized Universal Circuits for Secure Evaluation of Private Functions with Application to Data Classification"
      assert line[87] == r"title: The $F_f$-Family of Protocols for RFID-Privacy and Authentication"
      assert line[88] == r"title: The $n^c$-Unique Shortest Vector Problem is Hard"
      assert line[89] == r"title: A NEW HASH ALGORITHM$:$ Khichidi$-$1"
      assert line[90] == r"title: A Fast Implementation of $\eta _T$ Pairing in Characteristic Three on Intel Core 2 Duo Processor"
      assert line[91] == r"title: How to Prove the Security of Practical Cryptosystems with Merkle-Damgård Hashing by Adopting Indifferentiability"
      assert line[92] == r"title: Low Complexity Cubing and Cube Root Computation over $F_{3^m}$ in Polynomial Basis"
      assert line[93] == r"title: Practical Key Recovery Attack against Secret-preﬁx Edon-R"
      assert line[94] == r"title: A new bound for t−wise almost universal hash functions"
      assert line[95] == r"title: Indifferentiability with Distinguishers: Why Shabal\\Does Not Require Ideal Ciphers"
      assert line[96] == r"title: Hardware Implementations of a Variant of the Zémor-Tillich Hash Function: Can a Provably Secure Hash Function be very efficient ?"
      assert line[97] == r"title: On the Randomness and Regularity of Reduced EDON-$\protect \mathcal  {R}$ Compression Function"
      assert line[98] == r"title: Differential Path for SHA-1 with complexity $O(2^{52})$"
      assert line[99] == r"title: Algebraic Attacks specialized to \protect \(\protect \mathbb  {F}_2\protect \) (Diplomarbeit)"
      assert line[100] == r"title: FPGA Implementations of SHA-3 Candidates:CubeHash, Grøstl, L{\protect \sc  ane}, Shabal and Spectral Hash"
      assert line[101] == r"title: Compact Hardware Implementations of the SHA-3 Candidates ARIRANG, BLAKE, Grøstl, and Skein"
      assert line[102] == r"title: Cryptanalysis of the Tillich-Zémor hash function"
      assert line[103] == r"title: A short Note on Discrete Log Problem in $\protect \mathbb  {F_p}$"
      assert line[104] == r"title: Permutation Polynomials modulo $p^n$"
      assert line[105] == r"title: Fast Architectures for the $\eta _T$ Pairing over Small-Characteristic Supersingular Elliptic Curves"
      assert line[106] == r"title: A Secure and Efficient Authenticated Diffie–Hellman Protocol"
      assert line[107] == r"title: Ntr¹u-like Public Key Cryptosystems beyond Dedekind Domain Up to Alternative Algebra"
      assert line[108] == r"title: Improving the Berlekamp algorithm for binomials \protect \boldmath  $x^{n} - a$"
      assert line[109] == r"title: On Cryptographic Protocols Employing Asymmetric Pairings -- The Role of $\Psi $ Revisited"
      assert line[110] == r"title: Eﬃcient Privacy-Preserving Face Recognition"
      assert line[111] == r"title: High-Speed Hardware Implementations of BLAKE, Blue Midnight Wish, CubeHash, ECHO, Fugue, Grøstl, Hamsi, JH, Keccak, Luffa, Shabal, SHAvite-3, SIMD, and Skein"
      assert line[112] == r"title: A Family of $p$-ary Binomial Bent Functions"
      assert line[113] == r"title: A complete set of addition laws\\for incomplete Edwards curves"
      assert line[114] == r"title: Efficiency Limitations for $\Sigma $-Protocols for Group Homomorphisms"
      assert line[115] == r"title: Reducing Elliptic Curve Logarithm to Logarithm in a Finite Field $\protect \mathbb  {F}_q$ for Some Orders"
      assert line[116] == r"title: On the order of the polynomial $x^p-x-a$"
      assert line[117] == r"title: Constructing Veriﬁable Random Functions with Large Input Spaces"
      assert line[118] == r"title: On zero practical significance of “Key recovery attack on full GOST block cipher with zero time and memory”"
      assert line[119] == r"title: On The Broadcast and Validity-Checking Security of PKCS \#1 v1.5 Encryption"
      assert line[120] == r"title: Elliptic Curve Discrete Logarithm Problem over Small Degree Extension Fields. Application to the static Diffie-Hellman problem on $E(F_{q^5})$"
      assert line[121] == r"title: New Methods to Construct Golay Complementary Sequences Over the $QAM$ Constellation"
      assert line[122] == r"title: A Framework for Fully-Simulatable $t$-out-of-$n$ Oblivious Transfer"
      assert line[123] == r"title: A Security Weakness in Composite-Order Pairing-Based Protocols with Imbedding Degree $k>2$"
      assert line[124] == r"title: On second-order nonlinearities of some $\protect \mathcal  {D}_0$ type bent functions"
      assert line[125] == r"title: On the Indifferentiability of the Grøstl Hash Function"
      assert line[126] == r"title: The analytical property for $\zeta (s)$"
      assert line[127] == r"title: Combining leak--resistant arithmetic for elliptic curves defined over $F_p$ and RNS representation"
      assert line[128] == r"title: Fast Exhaustive Search for Polynomial Systems in $F_2$"
      assert line[129] == r"title: A Certifying Compiler for Zero-Knowledge Proofs of Knowledge Based on $\Sigma $-Protocols"
      assert line[130] == r"title: Decoding square-free Goppa codes over $F_p$"
      assert line[131] == r"title: Improved Collision Attacks on the Reduced-Round Grøstl Hash Function"
      assert line[132] == r"title: First-Order Side-Channel Attacks on the Permutation Tables Countermeasure –Extended Version–"
      assert line[133] == r"title: Perfectly Balanced Boolean Functions and Golić Conjecture"
      assert line[134] == r"title: Cryptanalysis and Improvement of A New Electronic Traveler’s Check Scheme Based on One-way Hash Function"
      assert line[135] == r"title: Two Attacks on Dutta’s Dynamic Group Key Agreement Protocol"
      assert line[136] == r"title: Eﬃcient Fully Secure Predicate Encryption for Conjunctions, Disjunctions and k-CNF/DNF formulae"
      assert line[137] == r"title: Number formula and degree level of ergodic polynomial functions over $\protect \mathbb  {Z}$/$2^{n}\protect \mathbb  {Z}$ and generalized result of linear equation on ergodic power-series T-Function"
      assert line[138] == r"title: Linear Approximations of Addition Modulo $2^n$-1"
      assert line[139] == r"title: RNS arithmetic in ${\protect \mathbb  F}_{p^k}$ and application to fast pairing computation"
      assert line[140] == r"title: On permutation polynomials EA-equivalent to the inverse function over $GF(2^n)$"
      assert line[141] == r"title: Fast Algorithm to solve a family of SIS problem with $l_\infty $ norm"
      assert line[142] == r"title: Enumerating Results of Homogeneous Rotation over $GF(p)$"
      assert line[143] == r"title: Practical Frameworks For $h$-Out-Of-$n$ Oblivious Transfer With Security Against Covert and Malicious Adversaries"
      assert line[144] == r"title: Cover and Decomposition Index Calculus on Elliptic Curves made practical. Application to a seemingly secure curve over $F_{p^6}$"
      assert line[145] == r"title: A Construction of A New Class of Knapsack-Type Public Key Cryptosystem, K(III)$\Sigma $PKC"
      assert line[146] == r"title: Ergodic Theory Over ${F}_2[[T]]$"
      assert line[147] == r"title: Computing $(\ell ,\ell )$-isogenies in polynomial time on Jacobians of genus\protect \nobreakspace  {}$2$ curves"
      assert line[148] == r"title: Linear Diophantine Equation Discrete Log Problem, Matrix Decomposition Problem and the AA{\beta }-cryptosystem"
      assert line[149] == r"title: On the relation between the MXL family of algorithms and Gröbner basis algorithms"
      assert line[150] == r"title: Security Analysis of $LMAP^{++}$, an RFID Authentication Protocol"
      assert line[151] == r"title: Cryptanalysis of Chen \protect \textit  {et al.}'s RFID Access Control Protocol"
      assert line[152] == r"title: On the Number of Carries Occuring in an Addition $\protect \mod  2^k-1$"
      assert line[153] == r"title: Security \& Indistinguishability in the Presence of Traffic Analysis"
      assert line[154] == r"title: Exploiting Linear Hull in Matsui’s Algorithm 1 (extended version)"
      assert line[155] == r"title: Scalar Multiplication on Koblitz Curves using $\tau ^2-$NAF"
      assert line[156] == r"title: Cryptanalysis of the Smart-Vercauteren and Gentry-Halevi’s Fully Homomorphic Encryption"
      assert line[157] == r"title: Simple and Asymptotically Optimal $t$-Cheater Identifiable Secret Sharing Scheme"
      assert line[158] == r"title: Cryptanalysis of Cho \protect \textit  {et al.}'s Protocol, A Hash-Based Mutual Authentication Protocol for RFID Systems"
      assert line[159] == r"title: $HB^N$: An HB-like protocol secure against man-in-the-middle attacks"
      assert line[160] == r"title: Cryptanalysis of the $AA_{\beta }$ Cryptosystem based on Linear Diophantine Equation Discrete Log Problem"
      assert line[161] == r"title: High-Entropy Visual Identiﬁcation for Touch Screen Devices"
      assert line[162] == r"title: The Value $4$ of Binary Kloosterman Sums"
      assert line[163] == r"title: A representation of the $p$-sylow subgroup of $PERM(F_p^n)$ and a cryptographic application"
      assert line[164] == r"title: On a generalized combinatorial conjecture involving addition $\protect \mod  2^k - 1$"
      assert line[165] == r"title: Cryptanalysis of improved Yeh \protect \textit  {et al. }'s authentication Protocol: An EPC Class-1 Generation-2 standard compliant protocol"
      assert line[166] == r"title: On the influence of the algebraic degree of $F^{−1}$ on the algebraic degree of $G \circ F$"
      assert line[167] == r"title: Efficient Implementation of the $\eta _T$ Pairing on GPU"
      assert line[168] == r"title: Randomness Extraction in finite fields $\protect \mathbb  {F}_{p^{n}}$"
      assert line[169] == r"title: Impact of Intel's New Instruction Sets on Software Implementation of $GF(2)[x]$ Multiplication"
      assert line[170] == r"title: Receipt Freeness of Prêt à Voter Provably Secure"
      assert line[171] == r"title: New Subexponential Algorithms for Factoring in $SL(2,F_q)$"
      assert line[172] == r"title: $GF(2^{n})$ Subquadratic Polynomial Basis Multipliers for Some Irreducible Trinomials"
      assert line[173] == r"title: A Scalable Method for Constructing Galois NLFSRs with Period $2^n-1$ using Cross-Join Pairs"
      assert line[174] == r"title: Constructing differentially 4-uniform permutations over $MBF_{2^{2m}}$ from quadratic APN permutations over $MBF_{2^{2m+1}}$"
      assert line[175] == r"title: Breaking $H^2$-MAC Using Birthday Paradox"
      assert line[176] == r"title: On the security of Lo et al.’s ownership transfer protocol"
      assert line[177] == r"title: Decoding Random Binary Linear Codes in $2^{n/20}$: How $1+1=0$ Improves Information Set Decoding"
      assert line[178] == r"title: Some results on $q$-ary bent functions"
      assert line[179] == r"title: Key Length Estimation of Pairing-based Cryptosystems using $\eta _T$ Pairing"
      assert line[180] == r"title: Modified version of “Latin Dances Revisited: New Analytic Results of Salsa20 and ChaCha”"
      assert line[181] == r"title: Construction of the Tsujii-Shamir-Kasahara (TSK) Type Multivariate Public Key Cryptosystem, which relies on the Diﬃculty of Prime Factorization"
      assert line[182] == r"title: (Pseudo) Preimage Attack on Round-Reduced Grøstl Hash Function and Others (Extended Version)"
      assert line[183] == r"title: Adaptive Preimage Resistance Analysis Revisited:\\ Requirements, Subtleties and Implications"
      assert line[184] == r"title: A General Construction for 1-round $\delta $-RMT and (0, $\delta $)-SMT"
      assert line[185] == r"title: New Transference Theorems on Lattices Possessing n^\epsilon -unique Shortest Vectors"
      assert line[186] == r"title: Construction of New Classes of Knapsack Type Public Key Cryptosystem Using Uniform Secret Sequence, K(II)$\Sigma \Pi $PKC, Constructed Based on Maximum Length Code"
      assert line[187] == r"title: Breaking pairing-based cryptosystems using $\eta _T$ pairing over $GF(3^{97})$"
      assert line[188] == r"title: Multiple Differential Cryptanalysis using LLRand $\chi ^2$ Statistics"
      assert line[189] == r"title: CCBKE – Session Key Negotiation for Fast and Secure Scheduling of Scientific Applications in Cloud Computing"
      assert line[190] == r"title: Cryptanalysis of Sood et al.’s Authentication Scheme using Smart Cards"
      assert line[191] == r"title: On second-order nonlinearity and maximum algebraic immunity of some bent functions in $c^PS^+$"
      assert line[192] == r"title: Low complexity bit-parallel $GF(2^m)$ multiplier for all-one polynomials"
      assert line[193] == r"title: A note on ‘An efficient certificateless aggregate signature with constant pairing computations’"
      assert line[194] == r"title: On the Simplicity of Converting Leakages from Multivariate to Univariate – Case Study of a Glitch-Resistant Masking Scheme –"
      assert line[195] == r"title: Tahoe – The Least-Authority Filesystem"
      assert line[196] == r"title: A Low-Area Unified Hardware Architecture for the AES and the Cryptographic Hash Function Grøstl"
      assert line[197] == r"title: Bit-Parallel $GF(2^{n})$ Squarer Using Shifted Polynomial Basis"
      assert line[198] == r"title: Practical Covertly Secure MPC for Dishonest Majority – or: Breaking the SPDZ Limits"
      assert line[199] == r"title: Asynchronous Physical Unclonable Functions – AsyncPUF"
      assert line[200] == r"title: Uniform Compression Functions Can Fail to Preserve “Full” Entropy"
      assert line[201] == r"title: Estimating the Φ(n) of Upper/Lower Bound in its RSA Cryptosystem"
      assert line[202] == r"title: Improved (Pseudo) Preimage Attack and Second Preimage Attack on Round-Reduced Grøstl"
      assert line[203] == r"title: New Impossible Differential Attack on $\protect \text  {SAFER}_{+}$ and $\protect \text  {SAFER}_{++}$"
      assert line[204] == r"title: On the Function Field Sieve and the Impact of Higher Splitting Probabilities: Application to Discrete Logarithms in $F_{2^{1971}}$ and $F_{2^{3164}}$"
      assert line[205] == r"title: A new index calculus algorithm with complexity $L(1/4+o(1))$ in very small characteristic"
      assert line[206] == r"title: Cryptanalysis of Some Double-Block-Length Hash Modes of Block Ciphers with $n$-Bit Block and $n$-Bit Key"
      assert line[207] == r"title: A New Class of Product-sum Type Public Key Cryptosystem,K(V)$\Sigma \Pi $PKC,Constructed Based on Maximum Length Code"
      assert line[208] == r"title: Practical and Employable Protocols for UC-Secure Circuit Evaluation over $Z_n$"
      assert line[209] == r"title: Attacks on JH, Grøstl and SMASH Hash Functions"
      assert line[210] == r"title: Adapting Lyubashevsky’s Signature Schemes to the Ring Signature Setting"
      assert line[211] == r"title: Theory of masking with codewords in hardware: low-weight $d$th-order correlation-immune Boolean functions"
      assert line[212] == r"title: Solving a $6120$-bit DLP on a Desktop Computer"
      assert line[213] == r"title: Security in $O(2^n)$ for the Xor of Two Random Permutations\\ -- Proof with the standard $H$ technique--"
      assert line[214] == r"title: Breaking the Even-Mansour Hash Function: Collision and Preimage Attacks on JH and Grøstl"
      assert line[215] == r"title: Key Recovery Attacks on 3-round Even-Mansour, 8-step LED-128, and Full $\protect \mbox  {AES}^{2}$"
      assert line[216] == r"title: Efficient Cryptosystems From $2^k$-th Power Residue Symbols"
      assert line[217] == r"title: Fast Exhaustive Search for Quadratic Systems in $\protect \mathbb  {F}_2$ on FPGAs --- Extended Version"
      assert line[218] == r"title: Revisiting Conditional Rényi Entropies and Generalizing Shannon's Bounds in Information Theoretically Secure Encryption"
      assert line[219] == r"title: Multi-Valued Byzantine Broadcast: the $t < n$ Case"
      assert line[220] == r"title: Self-pairings on supersingular elliptic curves with embedding degree $three$"
      assert line[221] == r"title: More Efficient Cryptosystems From $k^{th}$-Power Residues"
      assert line[222] == r"title: The Special Number Field Sieve in $F_{p^{n}}$, Application to Pairing-Friendly Constructions"
      assert line[223] == r"title: Solving the Elliptic Curve Discrete Logarithm Problem Using Semaev Polynomials, Weil Descent and Gröbner Basis Methods -- an Experimental Study"
      assert line[224] == r"title: Some results concerning global avalanche characteristics of two $q$-ary functions"
      assert line[225] == r"title: Stamp \& Extend -- Instant but Undeniable Timestamping based on Lazy Trees"
      assert line[226] == r"title: CBEAM: Efficient Authenticated Encryption from Feebly One-Way $\phi $ Functions"
      assert line[227] == r"title: $GF(2^n)$ Bit-Parallel Squarer Using Generalized Polynomial Basis For a New Class of Irreducible Pentanomials"
      assert line[228] == r"title: Construction of New Families of ‎MDS‎ Diffusion Layers"
      assert line[229] == r"title: Solving Random Subset Sum Problem by $l_{p}$-norm SVP Oracle"
      assert line[230] == r"title: Side-Channel Leakage through Static Power – Should We Care about in Practice? –"
      assert line[231] == r"title: Crypto-analyses on “user efficient recoverable off-line e-cashs scheme with fast anonymity revoking”"
      assert line[232] == r"title: Cryptanalysis on “Secure untraceable off-line electronic cash system”"
      assert line[233] == r"title: A Preliminary FPGA Implementation and Analysis of Phatak’s Quotient-First Scaling Algorithm in the Reduced-Precision Residue Number System"
      assert line[234] == r"title: Secure Compression: Theory \& Practice"
      assert line[235] == r"title: Breaking `128-bit Secure' Supersingular Binary Curves (or how to solve discrete logarithms in ${\protect \mathbb  F}_{2^{4 \cdot 1223}}$ and ${\protect \mathbb  F}_{2^{12 \cdot 367}}$)"
      assert line[236] == r"title: Generalized proper matrices and constructing of $m$-resilient Boolean functions with maximal nonlinearity for expanded range of parameters"
      assert line[237] == r"title: Remarks on the Pocklington and Padró-Sáez Cube Root Algorithm in $\protect \mathbb  F_q$"
      assert line[238] == r"title: Trial multiplication is not optimal but... On the symmetry of finite cyclic groups (Z/pZ)∗"
      assert line[239] == r"title: An Efficient Abuse-Free Fair Contract-Signing Protocol Based on RSA Signature and Σ-protocol"
      assert line[240] == r"title: Actively Private and Correct MPC Scheme in $t < n/2$ from Passively Secure Schemes with Small Overhead"
      assert line[241] == r"title: Collision Attack on 5 Rounds of Grøstl"
      assert line[242] == r"title: Proof of Activity: Extending Bitcoin’s Proof of Work via Proof of Stake"
      assert line[243] == r"title: Lightweight Diffusion Layer from the $k^{th}$ root of the MDS Matrix"
      assert line[244] == r"title: On the quaternion $\ell $-isogeny path problem"
      assert line[245] == r"title: New Classes of Public Key Cryptosystems over $F_2^8$ Constructed Based on Reed-Solomon Codes, K(XVII)SE(1)PKC and K(XVII)$\Sigma \Pi $PKC"
      assert line[246] == r"title: Simple AEAD Hardware Interface (SÆHI) in a SoC: Implementing an On-Chip Keyak/WhirlBob Coprocessor"
      assert line[247] == r"title: An Efficient $t$-Cheater Identifiable Secret Sharing Scheme with Optimal Cheater Resiliency"
      assert line[248] == r"title: Zipf’s Law in Passwords"
      assert line[249] == r"title: An Equivalent Condition on the Switching Construction of Differentially $4$-uniform Permutations on $GF_{2^{2k}}$ from the Inverse Function"
      assert line[250] == r"title: A Dynamic Cube Attack on $105$ round Grain v1"
      assert line[251] == r"title: On the Optimal Pre-Computation of Window $\tau $NAF for Koblitz Curves"
      assert line[252] == r"title: New Class of Multivariate Public Key Cryptosystem, K(XI)RSE(2)PKC, Constructed based on Reed-Solomon Code Along with K(X)RSE(2)PKC over $\protect \mathbb  {F}_2$"
      assert line[253] == r"title: Crypto-analyses on “secure and efficient privacy-preserving public auditing scheme for cloud storage”"
      assert line[254] == r"title: Navigating in the Cayley graph of $SL_2(F_p)$ and applications to hashing"
      assert line[255] == r"title: Faster ECC over $\protect \mathbb  {F}_{2^{521}-1}$"
      assert line[256] == r"title: Post-Quantum Forward-Secure Onion Routing (Future Anonymity in Today’s Budget)"
      assert line[257] == r"title: Optimal software-implemented Itoh--Tsujii inversion for GF($2^m$)"
      assert line[258] == r"title: Non-committing encryption from $\Phi $-hiding"
      assert line[259] == r"title: CamlCrush: A PKCS\#11 Filtering Proxy"
      assert line[260] == r"title: Fully Homomorphic Encryption from Ring-LWE：Identity-Based，Arbitrary Cyclotomic，Tighter Parameters"
      assert line[261] == r"title: Related-Key Forgeries for Prøst-OTR"
      assert line[262] == r"title: Déjà Q: Encore! Un Petit IBE"
      assert line[263] == r"title: C$\emptyset $C$\emptyset $: A Framework for Building Composable Zero-Knowledge Proofs"
      assert line[264] == r"title: Computing Jacobi's \theta in quasi-linear time"
      assert line[265] == r"title: Pseudo-Free Families of Finite Computational Elementary Abelian $p$-Groups"
      assert line[266] == r"title: Re-encryption Veriﬁability: How to Detect Malicious Activities of a Proxy in Proxy Re-encryption"
      assert line[267] == r"title: Tighter Security for Efficient Lattice Cryptography via the Rényi Divergence of Optimized Orders"
      assert line[268] == r"title: $\Lambda \circ \lambda $: Functional Lattice Cryptography"
      assert line[269] == r"title: A note on the optimality of frequency analysis vs. $\ell _p$-optimization"
      assert line[270] == r"title: Authenticated Range \& Closest Point Queries in Zero-Knowledge"
      assert line[271] == r"title: $Area-Time$ Efficient Hardware Implementation of Elliptic Curve Cryptosystem"
      assert line[272] == r"title: Unclonable encryption revisited ($4 \times 2 = 8$)"
      assert line[273] == r"title: Statistical Properties of Multiplication mod $2^n$"
      assert line[274] == r"title: Exhausting Demirci-Selçuk Meet-in-the-Middle Attacks against Reduced-Round AES"
      assert line[275] == r"title: Eclipse Attacks on Bitcoin’s Peer-to-Peer Network"
      assert line[276] == r"title: Identity-Set-based Broadcast Encryption supporting “Cut-or-Select” with Short Ciphertext"
      assert line[277] == r"title: End-to-End Verifiable Elections in the Standard Model∗"
      assert line[278] == r"title: New attacks on RSA with Moduli $N=p^rq$"
      assert line[279] == r"title: Improved security proofs in lattice-based cryptography: using the Rényi divergence rather than the statistical distance"
      assert line[280] == r"title: Improving algebraic attacks on stream ciphers based on linear feedback shifter registers over $F_{2^k}$"
      assert line[281] == r"title: Computing Individual Discrete Logarithms Faster in $GF(p^n)$"
      assert line[282] == r"title: Related-Key Rectangle Attack on Round-reduced \protect \textit  {Khudra} Block Cipher"
      assert line[283] == r"title: Quantum homomorphic encryption for circuits of low $T$-gate complexity"
      assert line[284] == r"title: PUDA – Privacy and Unforgeability for Data Aggregation"
      assert line[285] == r"title: Improved (Pseudo) Preimage Attacks on Reduced-Round GOST and Grøstl-256 and Studies on Several Truncation Patterns for AES-like Compression Functions (Full Version)"
      assert line[286] == r"title: An analysis of the $C$ class of bent functions"
      assert line[287] == r"title: Improved Linear Hull Attack on Round-Reduced \protect \textsc  {Simon} with Dynamic Key-guessing Techniques"
      assert line[288] == r"title: On Generating Coset Representatives of PGL_2(F_q) in PGL_2(F_{q^2})"
      assert line[289] == r"title: Interdiction in Practice – Hardware Trojan Against a High-Security USB Flash Drive"
      assert line[290] == r"title: Skipping the $q$ in Group Signatures"
      assert line[291] == r"title: Comparison of cube attacks over diﬀerent vector spaces"
      assert line[292] == r"title: Faster point scalar multiplication on NIST elliptic curves over GF(p) using (twisted) Edwards curves over GF(p³)"
      assert line[293] == r"title: Fast Oblivious AES\\A dedicated application of the MiniMac protocol"
      assert line[294] == r"title: Refund attacks on Bitcoin’s Payment Protocol"
      assert line[295] == r"title: Standard quantum bit commitment – an indefinite commitment time"
      assert line[296] == r"title: The Security of NTP’s Datagram Protocol"
      assert line[297] == r"title: An Algorithm for Counting the Number of $2^n$-Periodic Binary Sequences with Fixed $k$-Error Linear Complexity"
      assert line[298] == r"title: Construction of $n$-variable ($n\equiv 2 \protect \bmod  4$) balanced Boolean functions with maximum absolute value in autocorrelation spectra $< 2^{\protect \frac  n2}$"
      assert line[299] == r"title: Direct construction of quasi-involutory recursive-like MDS matrices from $2$-cyclic codes"
      assert line[300] == r"title: Modifying Shor’s algorithm to compute short discrete logarithms"
      assert line[301] == r"title: Are RNGs Achilles’ heel of RFID Security and Privacy Protocols ?"
      assert line[302] == r"title: Comments on “Flaw in the Security Analysis of Leakage-resilient Authenticated Key Exchange Protocol from CT-RSA 2016 and Restoring the Security Proof”"
      assert line[303] == r"title: An Oblivious Parallel RAM with $O(\log ^2 N)$ Parallel Runtime Blowup"
      assert line[304] == r"title: Computing Optimal Ate Pairings on Elliptic Curves with Embedding Degree $9,15$ and $27$"
      assert line[305] == r"title: Collecting relations for the Number Field Sieve in $GF(p^6)$"
      assert line[306] == r"title: A new algorithm for residue multiplication modulo $2^{521}-1$"
      assert line[307] == r"title: Cryptanalysis of Multi-Prime $\Phi $-Hiding Assumption"
      assert line[308] == r"title: Cryptographic Properties of Addition Modulo $2^n$"
      assert line[309] == r"title: Trick or Tweak: On the (In)security of OTR’s Tweaks"
      assert line[310] == r"title: May-Ozerov Algorithm for Nearest-Neighbor Problem over $\protect \mathbb  {F}_{q}$ and Its Application to Information Set Decoding"
      assert line[311] == r"title: \protect \(\mu \protect \)Kummer: efficient hyperelliptic signatures and key exchange on microcontrollers"
      assert line[312] == r"title: Malleability of the blockchain’s entropy"
      assert line[313] == r"title: Automatic Search for the Best Trails in ARX: Application to Block Cipher \protect \textsc  {Speck}"
      assert line[314] == r"title: A note on the security of threshold implementations with $d+1$ input shares"
      assert line[315] == r"title: Loop-Abort Faults on Lattice-Based Fiat–Shamir and Hash-and-Sign Signatures"
      assert line[316] == r"title: Improved Factorization of $N=p^rq^s$"
      assert line[317] == r"title: Bitstream Fault Injections (BiFI) – Automated Fault Attacks against SRAM-based FPGAs"
      assert line[318] == r"title: Efficient probabilistic algorithm for estimating the algebraic properties of Boolean functions for large $n$"
      assert line[319] == r"title: The Lightest 4x4 MDS Matrices over $GL(4,\protect \mathbb  {F}_2)$"
      assert line[320] == r"title: Software Benchmarking of the 2$^{\protect \text  {nd}}$ round CAESAR Candidates"
      assert line[321] == r"title: Cryptographic Voting — A Gentle Introduction"
      assert line[322] == r"title: Privately Matching $k$-mers"
      assert line[323] == r"title: A generalisation of Dillon's APN permutation with the best known differential and nonlinear properties for all fields of size $2^{4k+2}$"
      assert line[324] == r"title: Generalized Desynchronization Attack on UMAP: Application to RCIA, KMAP, SLAP and SASI$^+$ protocols"
      assert line[325] == r"title: Fast Arithmetic Modulo $2^xp^y\pm 1$"
      assert line[326] == r"title: Practical Non-Malleable Codes from $\ell $-more Extractable Hash Functions"
      assert line[327] == r"title: Fast Montgomery-like Square Root Computation over $GF(2^m)$ for All Trinomials"
      assert line[328] == r"title: Round and Communication Efficient Unconditionally-secure MPC with $t < n/3$ in Partially Synchronous Network"
      assert line[329] == r"title: Homomorphic SIM$^2$D Operations: Single Instruction Much More Data"
      assert line[330] == r"title: A Novel Pre-Computation Scheme of Window $\tau $NAF for Koblitz Curves"
      assert line[331] == r"title: $\mu $chain: How to Forget without Hard Forks"
      assert line[332] == r"title: Settling the mystery of $Z_r=r$ in RC4"
      assert line[333] == r"title: A Certain Family of Subgroups of $\protect \mathbb  Z_n^\star $ Is Weakly Pseudo-Free under the General Integer Factoring Intractability Assumption"
      assert line[334] == r"title: Machine-Learning Attacks on PolyPUFs, OB-PUFs, RPUFs, LHS-PUFs, and PUF–FSMs"
      assert line[335] == r"title: Twisted $\mu _4$-normal form for elliptic curves"
      assert line[336] == r"title: Quantum Demiric-Selçuk Meet-in-the-Middle Attacks: Applications to 6-Round Generic Feistel Constructions"
      assert line[337] == r"title: A Provably Secure PKCS\#11 Configuration Without Authenticated Attributes"
      assert line[338] == r"title: Some results on the existence of $t$-all-or-nothing transforms over arbitrary alphabets"
      assert line[339] == r"title: The Approximate $k$-List Problem"
      assert line[340] == r"title: Cryptanalysis of Wang et al’s Certificateless Signature Scheme without Bilinear Pairings"
      assert line[341] == r"title: When It’s All Just Too Much: Outsourcing MPC-Preprocessing"
      assert line[342] == r"title: A New Algorithm for Inversion mod $p^k$"
      assert line[343] == r"title: Efficient hash maps to \protect \mathbb  {G}_2 on BLS curves"
      assert line[344] == r"title: Sharper Bounds in Lattice-Based Cryptography using the Rényi Divergence"
      assert line[345] == r"title: Encryption Switching Protocols Revisited: Switching modulo $p$"
      assert line[346] == r"title: Recovering Short Generators of Principal Fractional Ideals in Cyclotomic Fields of Conductor $p^\alpha q^\beta $"
      assert line[347] == r"title: Snarky Signatures: \\ Minimal Signatures of Knowledge from Simulation-Extractable SNARKs"
      assert line[348] == r"title: Multiplication and Division over Extended Galois Field GF($p^q$): A new Approach to find Monic Irreducible Polynomials over any Galois Field GF($p^q$)."
      assert line[349] == r"title: Can You Trust Your Encrypted Cloud? An Assessment of SpiderOakONE’s Security"
      assert line[350] == r"title: Large Modulus Ring-LWE $\geq $ Module-LWE"
      assert line[351] == r"title: Brute–Force Search Strategies for Single–Trace and Few–Traces Template Attacks on the DES Round Keys of a Recent Smart Card"
      assert line[352] == r"title: Lower bounds on communication for multiparty computation of multiple «AND» instances with secret sharing"
      assert line[353] == r"title: δ-subgaussian Random Variables in Cryptography"
      assert line[354] == r"title: AS$^3$: Adaptive Social Secret Sharing for Distributed Storage Systems"
      assert line[355] == r"title: Lattice-Based Techniques for Accountable Anonymity: Composition of Abstract Stern’s Protocols and Weak PRF with Efficient Protocols from LWR"
      assert line[356] == r"title: HAL — The Missing Piece of the Puzzle for Hardware Reverse Engineering, Trojan Detection and Insertion"
      assert line[357] == r"title: No-Match Attacks and Robust Partnering Definitions – Defining Trivial Attacks for Security Protocols is Not Trivial"
      assert line[358] == r"title: Möbius: Trustless Tumbling for Transaction Privacy"
      assert line[359] == r"title: Blockwise $p$-Tampering Attacks on Cryptographic Primitives, Extractors, and Learners"
      assert line[360] == r"title: On the Power of Amortization in Secret Sharing: $d$-Uniform Secret Sharing and CDS with Constant Information Rate"
      assert line[361] == r"title: Full-Hiding (Unbounded) Multi-Input Inner Product Functional Encryption from the $k$-Linear Assumption"
      assert line[362] == r"title: Faster multiplication in $\protect \mathbb  {Z}_{2^m}[x]$ on Cortex-M4 to speed up NIST PQC candidates"
      assert line[363] == r"title: Synchronous Byzantine Agreement with Expected $O(1)$ Rounds, Expected $O(n^2)$ Communication, and Optimal Resilience"
      assert line[364] == r"title: Constructing Infinite Families of Low Differential Uniformity $(n,m)$-Functions with $m>n/2$"
      assert line[365] == r"title: Yet Another Size Record for AES: A First-Order SCA Secure AES S-box Based on GF($2^8$) Multiplication"
      assert line[366] == r"title: P4TC—Provably-Secure yet Practical Privacy-Preserving Toll Collection"
      assert line[367] == r"title: Improvements of Blockchain’s Block Broadcasting:An Incentive Approach"
      assert line[368] == r"title: On the Concrete Security of Goldreich’s Pseudorandom Generator"
      assert line[369] == r"title: Polynomial Time Bounded Distance Decoding near Minkowski’s Bound in Discrete Logarithm Lattices"
      assert line[370] == r"title: Full Indifferentiable Security of the Xor of Two or More Random Permutations Using the $\chi ^2$ Method"
      assert line[371] == r"title: Can We Overcome the $n \log n$ Barrier for Oblivious Sorting?"
      assert line[372] == r"title: Hadamard Matrices, $d$-Linearly Independent Sets and Correlation-Immune Boolean Functions with Minimum Hamming Weights"
      assert line[373] == r"title: Agreement with Satoshi – On the Formalization of Nakamoto Consensus"
      assert line[374] == r"title: “Larger Keys, Less Complexity” A Strategic Proposition"
      assert line[375] == r"title: Efficient Range ORAM with $\protect \mathbb  {O}(\log ^{2}{N})$ Locality"
      assert line[376] == r"title: Improved Parallel Mask Refreshing Algorithms: Generic Solutions with Parametrized Non-Interference \& Automated Optimizations"
      assert line[377] == r"title: Finding Small Solutions of the Equation $Bx-Ay=z$ and Its Applications to Cryptanalysis of the RSA Cryptosystem"
      assert line[378] == r"title: On the Menezes-Teske-Weng’s conjecture"
      assert line[379] == r"title: A $k$-out-of-$n$ Ring Signature with Flexible Participation for Signers"
      assert line[380] == r"title: Towards Static Assumption Based Cryptosystem in Pairing Setting: Further Applications of DéjàQ and Dual-Form Signature"
      assert line[381] == r"title: Witness-Indistinguishable Arguments with $\Sigma $-Protocols for Bundled Witness Spaces and its Application to Global Identities"
      assert line[382] == r"title: Practical Fully Secure Unrestricted Inner Product Functional Encryption modulo $p$"
      assert line[383] == r"title: Blending FHE-NTRU keys – The Excalibur Property"
      assert line[384] == r"title: Injective Trapdoor Functions via Derandomization: How Strong is Rudich’s Black-Box Barrier?"
      assert line[385] == r"title: Programming the Demirci-Sel{ç}uk Meet-in-the-Middle Attack with Constraints"
      assert line[386] == r"title: Building Quantum-One-Way Functions from Block Ciphers: Davies-Meyer and Merkle-Damgård Constructions"
      assert line[387] == r"title: Round Optimal Black-Box “Commit-and-Prove”"
      assert line[388] == r"title: How to leverage hardness of constant-degree expanding polynomials over $\protect \mathbb  {R}$ to build iO"
      assert line[389] == r"title: A Proof of the Beierle-Kranz-Leander’s Conjecture related to Lightweight Multiplication in $F_{2^n}$"
      assert line[390] == r"title: Upper Bound on $\lambda _1(\Lambda ^{\bot }(\protect \mathbf  A))$"
      assert line[391] == r"title: Quantum Algorithms for the Approximate $k$-List Problem and their Application to Lattice Sieving"
      assert line[392] == r"title: Breaking the Bluetooth Pairing – The Fixed Coordinate Invalid Curve Attack"
      assert line[393] == r"title: New point compression method for elliptic $\protect \mathbb  {F}_{\protect \!q^2}$-curves of $j$-invariant $0$"
      assert line[394] == r"title: Low Complexity MDS Matrices Using $GF(2^n)$ SPB or GPB"
      assert line[395] == r"title: On the Complexity of non-recursive $n$-term Karatsuba Multiplier for Trinomials"
      assert line[396] == r"title: Formalising $\Sigma $-Protocols and Commitment Schemes using CryptHOL"
      assert line[397] == r"title: Simplifying Constructions and Assumptions for $i\protect \mathcal  {O}$"
      assert line[398] == r"title: Probabilistic Properties of Modular Addition \\ (Extended abstract)"
      assert line[399] == r"title: Fast Secrecy Computation with Multiplication Under the Setting of $k\le N<2k-1$ using Secret Sharing Scheme"
      assert line[400] == r"title: SÉTA: Supersingular Encryption from Torsion Attacks"
      assert line[401] == r"title: Hashing to elliptic curves of $j$-invariant $1728$"
      assert line[402] == r"title: Reduction Modulo $2^{448}-2^{224}-1$"
      assert line[403] == r"title: Unifying Leakage Models on a Rényi Day"
      assert line[404] == r"title: Toward A More Efficient Gröbner-based Algebraic Cryptanalysis"
      assert line[405] == r"title: $AC^0$ Constructions for Evolving Secret Sharing Schemes and Redistribution of Secret Shares"
      assert line[406] == r"title: Analogue of Vélu's Formulas for Computing Isogenies over Hessian Model of Elliptic Curves"
      assert line[407] == r"title: Solving $X^{q+1}+X+a=0$ over Finite Fields"
      assert line[408] == r"title: Overdrive2k: Efficient Secure MPC over $Z_{2^k}$ from Somewhat Homomorphic Encryption"
      assert line[409] == r"title: Fast Algebraic Immunity of $2^m+2$ & $2^m+3$ variables Majority Function"
      assert line[410] == r"title: Solving $x^{2^k+1}+x+a=0$ in $\protect \mathbb  {F}_{2^n}$ with $\gcd (n,k)=1$"
      assert line[411] == r"title: Fully Secure Attribute-Based Encryption for $t$-CNF from LWE"
      assert line[412] == r"title: Improving Speed of Dilithium’s Signing Procedure"
      assert line[413] == r"title: FloodXMR: Low-cost transaction flooding attack with Monero’s bulletproof protocol"
      assert line[414] == r"title: How to wrap it up - A formally verified proposal for the use of authenticated wrapping in PKCS\#11"
      assert line[415] == r"title: RingCT 3.0 for Blockchain Conﬁdential Transaction: Shorter Size and Stronger Security"
      assert line[416] == r"title: Solutions of $x^{q^k}+\protect \cdots  +x^{q}+x=a$ in $GF(2^n)$"
      assert line[417] == r"title: A${^2}$L: Anonymous Atomic Locks for Scalability in Payment Channel Hubs"
      assert line[418] == r"title: The Exchange Attack: How to Distinguish Six Rounds of AES with $2^{88.2}$ chosen plaintexts"
      assert line[419] == r"title: Scrutinizing the Tower Field Implementation of the $\protect \mathbb  {F}_{2^8}$ Inverter -- with Applications to AES, Camellia, and SM4"
      assert line[420] == r"title: On cryptographic parameters of permutation polynomials of the form $x^rh(x^{(q-1)/d})$"
      assert line[421] == r"title: Don't forget your roots: constant-time root finding over $\protect \mathbb  {F}_{2^m}$"
      assert line[422] == r"title: Can we Beat the Square Root Bound for ECDLP over $\protect \mathbb  {F}_{p^2}$ via Representations?"
      assert line[423] == r"title: Asymptotically-Good Arithmetic Secret Sharing over Z/(p^\ell Z) with Strong Multiplication and Its Applications to Efficient MPC"
      assert line[424] == r"title: Efficient Information-Theoretic Secure Multiparty Computation over $\protect \mathbb  {Z}/p^k \protect \mathbb  {Z}$ via Galois Rings"
      assert line[425] == r"title: Modifying The Tropical Version of Stickel’s Key Exchange Protocol"
      assert line[426] == r"title: One Bit is All It Takes: A Devastating Timing Attack on BLISS’s Non-Constant Time Sign Flips"
      assert line[427] == r"title: Probabilistic analysis on Macaulay matrices over finite fields and complexity of constructing Gröbner bases"
      assert line[428] == r"title: Information Conservational Security with “Black Hole” Keypad Compression and Scalable One-Time Pad — An Analytical Quantum Intelligence Approach to Pre- and Post-Quantum Cryptography"
      assert line[429] == r"title: Detecting Faults in Inner Product Masking Scheme - IPM-FD: IPM with Fault Detection (extended version∗)"
      assert line[430] == r"title: Low Weight Discrete Logarithms and Subset Sum in $2^{0.65n}$ with Polynomial Memory"
      assert line[431] == r"title: CCA-Secure Leakage-Resilient Identity-Based Key-Encapsulation from Simple (not $\protect \mathtt  {q}$-type) Assumptions"
      assert line[432] == r"title: Faster point compression for elliptic curves of $j$-invariant $0$"
      assert line[433] == r"title: Cortex-M4 Optimizations for \{R,M\}LWE Schemes"
      assert line[434] == r"title: Efficient indifferentiable hashing to elliptic curves $y^2 = x^3 + b$ provided that $b$ is a quadratic residue"
      assert line[435] == r"title: Karatsuba-based square-root Vélu’s formulas applied to two isogeny-based protocols"
      assert line[436] == r"title: Two-round $n$-out-of-$n$ and Multi-Signatures and Trapdoor Commitment from Lattices"
      assert line[437] == r"title: TinyGarble2: Smart, Efficient, and Scalable Yao’s Garble Circuit"
      assert line[438] == r"title: Schrödinger's Pirate: How To Trace a Quantum Decoder"
      assert line[439] == r"title: Cryptanalysis of RSA: A Special Case of Boneh-Durfee’s Attack"
      assert line[440] == r"title: Post-Quantum Cryptography with Contemporary Co-Processors: Beyond Kronecker, Schönhage-Strassen & Nussbaumer"
      assert line[441] == r"title: Simulation Extractable Versions of Groth’s zk-SNARK Revisited"
      assert line[442] == r"title: Breaking the $O(\protect \sqrt  n)$-Bit Barrier: Byzantine Agreement with Polylog Bits Per Party"
      assert line[443] == r"title: A New Generalisation of the Goldwasser-Micali Cryptosystem Based on the Gap $2^k$-Residuosity Assumption"
      assert line[444] == r"title: Compressed $\Sigma $-Protocols for Bilinear Group Arithmetic Circuits and Application to Logarithmic Transparent Threshold Signatures"
      assert line[445] == r"title: Cryptanalysis of Aggregate $\Gamma $-Signature and Practical Countermeasures in Application to Bitcoin"
      assert line[446] == r"title: Unlinkable and Invisible γ-Sanitizable Signatures"
      assert line[447] == r"title: The SQALE of CSIDH: Sublinear Vélu Quantum-resistant isogeny Action with Low Exponents"
      assert line[448] == r"title: Compressed $\Sigma $-Protocol Theory and Practical Application to Plug & Play Secure Algorithmics"
      assert line[449] == r"title: Comments on “ Multi Recipient Aggregate Signcryption Scheme Based on Elliptic Curve”"
      assert line[450] == r"title: Homological Characterization of bounded $F_2$-regularity"
      assert line[451] == r"title: $P_4$-free Partition and Cover Numbers and Application"
      assert line[452] == r"title: $L_1$-Norm Ball for CSIDH: Optimal Strategy for Choosing the Secret Key Space"
      assert line[453] == r"title: Bitcoin Crypto–Bounties for Quantum Capable Adversaries"
      assert line[454] == r"title: Committing to Quantum Resistance, Better: A Speed–and–Risk–Configurable Defence for Bitcoin against a Fast Quantum Computing Attack"
      assert line[455] == r"title: About the Tu-Deng Conjecture for $W(t)$ Less Than or Equal to 10"
      assert line[456] == r"title: On Adaptive Attacks against Jao-Urbanik’s Isogeny-Based Protocol"
      assert line[457] == r"title: New Assumptions and Efficient Cryptosystems from the $e$-th Power Residue Symbol"
      assert line[458] == r"title: A ”Final” Security Bug"
      assert line[459] == r"title: Multichain-MWPoW: A $p/2$ Adversary Power Resistant Blockchain Sharding Approach to a Decentralised Autonomous Organisation Architecture"
      assert line[460] == r"title: A Trace Based $GF(2^n)$ Inversion Algorithm"
      assert line[461] == r"title: ConTra Corona: Contact Tracing against the Coronavirus by Bridging the Centralized–Decentralized Divide for Stronger Privacy"
      assert line[462] == r"title: HACL×N: Verified Generic SIMD Crypto (for all your favorite platforms)"
      assert line[463] == r"title: MoniPoly---An Expressive $q$-SDH-Based Anonymous Attribute-Based Credential System"
      assert line[464] == r"title: Proof of Mirror Theory for $\xi _{\max }=2$"
      assert line[465] == r"title: Compressing Proofs of $k$-Out-Of-$n$ Partial Knowledge"
      assert line[466] == r"title: Functional Encryption for Attribute-Weighted Sums from $k$-Lin"
      assert line[467] == r"title: Time-Space Tradeoffs and Short Collisions in Merkle-Damgård Hash Functions"
      assert line[468] == r"title: Trace-$\Sigma $: a privacy-preserving contact tracing app"
      assert line[469] == r"title: Not enough LESS: An improved algorithm for solving Code Equivalence Problems over $\protect \mathbb  {F}_q$"
      assert line[470] == r"title: Secure merge with $O(n \log \log n)$ secure operation"
      assert line[471] == r"title: Cryptanalysis of a ``Strengthened'' Key Exchange Protocol for IoT, or When SAKE$^+$ Turns Out to Be SAKE$^-$"
      assert line[472] == r"title: Adaptively Secure Revocable Hierarchical IBE from $k$-linear Assumption"
      assert line[473] == r"title: Another code-based adaptation of Lyubashevsky’s signature cryptanalysed"
      assert line[474] == r"title: A Note on Authenticated Group Key Agreement Protocol Based on Twist Conjugacy Problem in Near – Rings"
      assert line[475] == r"title: Timing attacks and local timing attacks against Barrett’s modular multiplication algorithm"
      assert line[476] == r"title: New Techniques for Traitor Tracing: Size $N^{1/3}$ and More from Pairings"
      assert line[477] == r"title: Hashing to elliptic curves of $j=0$ and quadratic imaginary orders of class number $2$"
      assert line[478] == r"title: A Family of Nonlinear MDS Diffusion Layers over $\protect \mathbb  {F}_{2^{4n}}$"
      assert line[479] == r"title: Complete solution over $GF{p^n}$ of the equation $X^{p^k+1}+X+a=0$"
      assert line[480] == r"title: Evolution of Bulletin Board & its application to E-Voting – A Survey"
      assert line[481] == r"title: The Study of Modulo $2^n$"
      assert line[482] == r"title: SCA-secure ECC in software – mission impossible?"
      assert line[483] == r"title: Limits of Polynomial Packings for $\protect \mathbb  {Z}_{p^k}$ and $\protect \mathbb  {F}_{p^k}$"
      assert line[484] == r"title: Optimal encodings to elliptic curves of $j$-invariants $0$, $1728$"
      assert line[485] == r"title: Neyman’s Smoothness Test: a Trade-off between Moment-based and Distribution-based Leakage Detections"
      assert line[486] == r"title: Comparing Lattice Families for Bounded Distance Decoding near Minkowski’s Bound."
      assert line[487] == r"title: Discovering New $L$-Function Relations Using Algebraic Sieving"
      assert line[488] == r"title: Cairo – a Turing-complete STARK-friendly CPU architecture"
      assert line[489] == r"title: Glowworm Attack: Optical TEMPEST Sound Recovery via a Device’s Power Indicator LED"
      assert line[490] == r"title: Towards the Least Inequalities for Describing a Subset in $Z_2^n$"
      assert line[491] == r"title: A note on group membership tests for $G_1$, $G_2$ and $G_T$ on BLS pairing-friendly curves"
      assert line[492] == r"title: Facial Recognition for Remote Electronic Voting – Missing Piece of the Puzzle or Yet Another Liability?"
      assert line[493] == r"title: ($\epsilon ,\delta $)-indistinguishable Mixing for Cryptocurrencies"
      assert line[494] == r"title: Estimating (Miner) Extractable Value is Hard, Let’s Go Shopping!"
      assert line[495] == r"title: Gröbner Basis Attack on STARK-Friendly Symmetric-Key Primitives: JARVIS, MiMC and GMiMCerf"
      assert line[496] == r"title: Parallel Repetition of $(k_1,\protect \dots  ,k_{\mu })$-Special-Sound Multi-Round Interactive Proofs"
      assert line[497] == r"title: An Open Problem on the Bentness of Mesnager’s Functions"
      assert line[498] == r"title: Ofelimos: Combinatorial Optimization via Proof-of-Useful-Work \\ A Provably Secure Blockchain Protocol"
      assert line[499] == r"title: MHz2k: MPC from HE over $\protect \mathbb  {Z}_{2^k}$ with New Packing, Simpler Reshare, and Better ZKP"
      assert line[500] == r"title: Log-$\protect \mathcal  {S}$-unit lattices using Explicit Stickelberger Generators to solve Approx Ideal-SVP"
      assert line[501] == r"title: Fiat–Shamir Bulletproofs are Non-Malleable (in the Algebraic Group Model)"
      assert line[502] == r"title: Breaking the $IKEp182 Challenge"
      assert line[503] == r"title: On Bitcoin Cash’s Target Recalculation Functions"
      assert line[504] == r"title: $P/poly$ Invalidity of the Agr17 Functional Encryption Scheme"
      assert line[505] == r"title: \protect \(\chi \protect \)perbp: a Cloud-based Lightweight Mutual Authentication Protocol"
      assert line[506] == r"title: A State-Separating Proof for Yao’s Garbling Scheme"
      assert line[507] == r"title: Interactive Error Correcting Codes Over Binary Erasure Channels Resilient to $>\protect \frac  12$ Adversarial Corruption"
      assert line[508] == r"title: Practical Garbled RAM: GRAM with $O(\log ^2 n)$ Overhead"
      assert line[509] == r"title: Just how hard are rotations of $\protect \mathbb  {Z}^n$? Algorithms and cryptography with the simplest lattice"
      assert line[510] == r"title: Generating cryptographically-strong random lattice bases and recognizing rotations of $\protect \mathbb  {Z}^n$"
      assert line[511] == r"title: Improved Security Bound of \protect \textsf  {(E/D)WCDM}"
      assert line[512] == r"title: The most efficient indifferentiable hashing to elliptic curves of $j$-invariant $1728$"
      assert line[513] == r"title: Secure Sampling of Constant-Weight Words – Application to BIKE"
      assert line[514] == r"title: A Simple Deterministic Algorithm for Systems of Quadratic Polynomials over $\protect \mathbb  {F}_2$"
      assert line[515] == r"title: “They’re not that hard to mitigate”: What Cryptographic Library Developers Think About Timing Attacks"
      assert line[516] == r"title: Information Security in the Quantum Era. Threats to modern cryptography: Grover’s algorithm"
      assert line[517] == r"title: Improving Support-Minors rank attacks: applications to G$e$MSS and Rainbow"
      assert line[518] == r"title: Invertible Quadratic Non-Linear Layers for MPC-/FHE-/ZK-Friendly Schemes over $\protect \mathbb  F_p^n$"
      assert line[519] == r"title: Pre-Computation Scheme of Window $\tau $NAF for Koblitz Curves Revisited"
      assert line[520] == r"title: Tight Security Bounds for Micali’s SNARGs"
      assert line[521] == r"title: Indifferentiable hashing to ordinary elliptic $\protect \mathbb  {F}_{\protect \!q}$-curves of $j=0$ with the cost of one exponentiation in $\protect \mathbb  {F}_{\protect \!q}$"
      assert line[522] == r"title: A Compressed $\Sigma $-Protocol Theory for Lattices"
      assert line[523] == r"title: An $O(\log ^2 p)$ Approach to Point-Counting on Elliptic Curves From a Prominent Family Over the Prime Field $\protect \mathbb  {F}_p$"
      assert line[524] == r"title: Explicit connections between supersingular isogeny graphs and Bruhat–Tits trees"
      assert line[525] == r"title: Stacking Sigmas: A Framework to Compose $\Sigma $-Protocols for Disjunctions"
      assert line[526] == r"title: Let’s Take it Offline: Boosting Brute-Force Attacks on iPhone’s User Authentication through SCA"
      assert line[527] == r"title: Upslices, Downslices, and Secret-Sharing with Complexity of $1.5^n$"
      assert line[528] == r"title: CryptoGram: Fast Private Calculations of Histograms over Multiple Users’ Inputs"
      assert line[529] == r"title: Cryptanalysis of Boyen’s Attribute-Based Encryption Scheme in TCC 2013"
      assert line[530] == r"title: Delegating Supersingular Isogenies over $\protect \mathbb  {F}_{p^2}$ with Cryptographic Applications"
      assert line[531] == r"title: LogStack: Stacked Garbling with $O(b \log b)$ Computation"
      assert line[532] == r"title: On the Possibility of Basing Cryptography on $EXP\protect \neq  BPP$"
      assert line[533] == r"title: Efficient Sorting of Homomorphic Encrypted Data with $k$-way Sorting Network"
      assert line[534] == r"title: Grover on Caesar and Vigenère Ciphers"
      assert line[535] == r"title: PrORAM: Fast $O(\log n)$ Private Coin ZK ORAM"
      assert line[536] == r"title: Side Channel Analysis against the ANSSI’s protected AES implementation on ARM"
      assert line[537] == r"title: Help, my Signal has bad Device! Breaking the Signal Messenger’s Post-CompromiseSecurity through a Malicious Device"
      assert line[538] == r"title: On the Design and Misuse of Microcoded (Embedded) Processors — A Cautionary Note"
      assert line[539] == r"title: Faster indifferentiable hashing to elliptic $\protect \mathbb  {F}_{\protect \!q^2}$-curves"
      assert line[540] == r"title: Learnability of Multiplexer PUF and $S_N$-PUF : A Fourier-based Approach"
      assert line[541] == r"title: GenoPPML – a framework for genomic privacy-preserving machine learning"
      assert line[542] == r"title: Appenzeller to Brie: Efficient Zero-Knowledge Proofs for Mixed-Mode Arithmetic and $\protect \mathbb  {Z}_{2^k}$"
      assert line[543] == r"title: A Note on ``Reduction Modulo $2^{448}-2^{224}-1$''"
      assert line[544] == r"title: SNARGs for $\protect \mathcal  {P}$ from LWE"
      assert line[545] == r"title: One-out-of-$q$ OT Combiners"
      assert line[546] == r"title: MPC for $Q_2$ Access Structures over Rings and Fields"
      assert line[547] == r"title: SoK: Gröbner Basis Algorithms for Arithmetization Oriented Ciphers"
      assert line[548] == r"title: Efficiency through Diversity in Ensemble Models applied to Side-Channel Attacks – A Case Study on Public-Key Algorithms –"
      assert line[549] == r"title: Tighter Security for Schnorr Identification and Signatures: A High-Moment Forking Lemma for $\Sigma $-Protocols"
      assert line[550] == r"title: SPHINCS-$\alpha $: A Compact Stateless Hash-Based Signature Scheme"
      assert line[551] == r"title: NTRU-$\nu $-um: Secure Fully Homomorphic Encryption from NTRU with Small Modulus"
      assert line[552] == r"title: Quantum Cryptanalysis of $5$ rounds Feistel schemes and Benes schemes"
      assert line[553] == r"title: Evaluating the Security of Merkle-Damgård Hash Functions and Combiners in Quantum Settings"
      assert line[554] == r"title: On NTRU-ν-um Modulo $X^N − 1$"
      assert line[555] == r"title: $\mu $Cash: Transparent Anonymous Transactions"
      assert line[556] == r"title: Arithmetization of Σ¹₁ relations with polynomial bounds in Halo 2"
      assert line[557] == r"title: Explicit infinite families of bent functions outside $\protect \mathcal  {MM}^\#$"
      assert line[558] == r"title: Threshold Linearly Homomorphic Encryption on $\protect \mathbf  {Z}/2^k\protect \mathbf  {Z}$"
      assert line[559] == r"title: The Scholz conjecture on addition chain is true for $v(n)= 4$"
      assert line[560] == r"title: On the Performance Gap of a Generic C Optimized Assembler and Wide Vector Extensions for Masked Software with an Ascon-{\protect \it  {p}} test case"
      assert line[561] == r"title: Second-Order Low-Randomness $d+1$ Hardware Sharing of the AES"
      assert line[562] == r"title: Bounded Surjective Quadratic Functions over $\protect \mathbb  F_p^n$ for MPC-/ZK-/FHE-Friendly Symmetric Primitives"
      assert line[563] == r"title: Hitchhiker’s Guide to a Practical Automated TFHE Parameter Setup for Custom Applications"
      assert line[564] == r"title: On Polynomial Functions Modulo $p^e$ and Faster Bootstrapping for Homomorphic Encryption"
      assert line[565] == r"title: Weightwise almost perfectly balanced functions: secondary constructions for all $n$ and better weightwise nonlinearities"
      assert line[566] == r"title: How to Meet Ternary LWE Keys on Babai’s Nearest Plane"
      assert line[567] == r"title: K-XMSS and K-SPHINCS$^+$:Hash based Signatures with\\Korean Cryptography Algorithms"
      assert line[568] == r"title: DAG-$\Sigma $: A DAG-based Sigma Protocol for Relations in CNF"
      assert line[569] == r"title: Applications of the indirect sum in the design of several special classes of bent functions outside the completed $\protect \mathcal  {MM}$ class"
      assert line[570] == r"title: Polynomial-Time Cryptanalysis of the Subspace Flooding Assumption for Post-Quantum $i\protect \mathcal  {O}$"
      assert line[571] == r"title: An algorithm for efficient detection of $(N,N)$-splittings and its application to the isogeny problem in dimension 2"
      assert line[572] == r"title: Demystifying the comments made on “A Practical Full Key Recovery Attack on TFHE and FHEW by Inducing Decryption Errors”"
      assert line[573] == r"title: Vector Commitments over Rings and Compressed $\Sigma $-Protocols"
      assert line[574] == r'title: NanoGRAM: Garbled RAM with $\setbox \z@ \hbox {\mathsurround \z@ $\textstyle O$}\mathaccent "0365{O}(\log N)$ Overhead'
      assert line[575] == r"title: Guaranteed Output in $O(\protect \sqrt  {n})$ Rounds for Round-Robin Sampling Protocols"
      assert line[576] == r"title: Promise $\Sigma $-protocol: How to Construct Efficient Threshold ECDSA from Encryptions Based on Class Groups"
      assert line[577] == r"title: On Time-Space Tradeoffs for Bounded-Length Collisions in Merkle-Damgård Hashing"
      assert line[578] == r"title: Beyond the Csiszár-Körner Bound: Best-Possible Wiretap Coding via Obfuscation"
      assert line[579] == r"title: Recovering the tight security proof of $SPHINCS^{+}$"
      assert line[580] == r"title: Fast Subgroup Membership Testings for $\protect \mathbb  {G}_1$, $\protect \mathbb  {G}_2$ and $\protect \mathbb  {G}_T$ on Pairing-friendly Curves"
      assert line[581] == r"title: An Improved Model on the Vague Sets-Based DPoS’s Voting Phase in Blockchain"
      assert line[582] == r"title: The Inverse of $\chi $ and Its Applications to Rasta-like Ciphers"
      assert line[583] == r"title: New optimization techniques for PlonK’s arithmetization"
      assert line[584] == r"title: Băhēm: A Provably Secure Symmetric Cipher"
      assert line[585] == r"title: India’s “Aadhaar” Biometric ID: Structure, Security, and Vulnerabilities"
      assert line[586] == r"title: Drive (Quantum) Safe! – Towards PQ Authentication for V2V Communications"
      assert line[587] == r"title: Two new classes of permutation trinomials over $\protect \mathbb  {F}_{q^3}$ with odd characteristic"
      assert line[588] == r"title: Don’t Learn What You Already Know: Scheme-Aware Modeling for Profiling Side-Channel Analysis against Masking"
      assert line[589] == r"title: Single-Trace Side-Channel Attacks on ω-Small Polynomial Sampling: With Applications to NTRU, NTRU Prime, and CRYSTALS-DILITHIUM"
      assert line[590] == r"title: Băhēm: A Symmetric Cipher with Provable 128-bit Security"
      assert line[591] == r"title: The Generals’ Scuttlebutt: Byzantine-Resilient Gossip Protocols"
      assert line[592] == r"title: Byzantine Reliable Broadcast with $O(nL+kn+n^2 log n)$ Communication"
      assert line[593] == r"title: Find the Bad Apples: An efficient method for perfect key recovery under imperfect SCA oracles – A case study of Kyber"
      assert line[594] == r"title: On the Differential Spectrum of a Differentially $3$-Uniform Power Function"
      assert line[595] == r"title: The $c-$differential uniformity and boomerang uniformity of three classes of permutation polynomials over $\protect \mathbb  {F}_{2^n}$"
      assert line[596] == r"title: Proof of Mirror Theory for a Wide Range of $\xi _{\max }$"
      assert line[597] == r"title: Tight Multi-User Security Bound of $\protect \textsf  {DbHtS}$"
      assert line[598] == r"title: LIKE – Lattice Isomorphism-based Non-Interactive Key Exchange via Group Actions"
      assert line[599] == r"title: Breaking the quadratic barrier: Quantum cryptanalysis of Milenage, telecommunications’ cryptographic backbone"
      assert line[600] == r"title: SwiftEC: Shallue–van de Woestijne Indifferentiable Function To Elliptic Curves"
      assert line[601] == r"title: Arithmetization of Σ¹₁ relations in Halo 2"
      assert line[602] == r"title: Simon’s Algorithm and Symmetric Crypto: Generalizations and Automatized Applications"
      assert line[603] == r"title: More Efficient Dishonest Majority Secure Computation over $\protect \mathbb  {Z}_{2^k}$ via Galois Rings"
      assert line[604] == r"title: Moz$\protect \mathbb  {Z}_{2^k}$arella: Efficient Vector-OLE and Zero-Knowledge Proofs Over $\protect \mathbb  {Z}_{2^k}$"
      assert line[605] == r"title: \protect \(\protect \texttt  {POLKA}\protect \): Towards Leakage-Resistant Post-Quantum CCA-Secure Public Key Encryption"
      assert line[606] == r"title: $\protect \texttt  {zk-creds}$: Flexible Anonymous Credentials from zkSNARKs and Existing Identity Infrastructure"
      assert line[607] == r"title: Efficient supersingularity testing over $\protect \mathbb  {F}_p$ and CSIDH key validation"
      assert line[608] == r"title: Time-Space Lower Bounds for Finding Collisions in Merkle-Damgård Hash Functions"
      assert line[609] == r"title: Post-quantum hash functions using $\protect \mathrm  {SL}_n(\protect \mathbb  {F}_p)$"
      assert line[610] == r"title: Low-Delay 4, 5 and 6-Term Karatsuba Formulae in $\protect \mathbb  {F}_2[x]$ Using Overlap-free Splitting"
      assert line[611] == r"title: MR-DSS – Smaller MinRank-based (Ring-)Signatures"
      assert line[612] == r"title: A Signature-Based Gröbner Basis Algorithm with Tail-Reduced Reductors (M5GB)"
      assert line[613] == r"title: An $\protect \mathcal  {O}(n)$ Algorithm for Coefficient Grouping"
      assert line[614] == r"title: Fast Hashing to $G_2$ in Direct Anonymous Attestation"
      assert line[615] == r"title: The Scholz conjecture on addition chain is true for infinitely many integers with ℓ(2n) = ℓ(n)"
      assert line[616] == r"title: Verification of the (1–δ)-Correctness Proof of CRYSTALS-KYBER with Number Theoretic Transform"
      assert line[617] == r"title: Grotto: Screaming fast $(2 + 1)$-PC for $\protect \mathbb  {Z}_{2^{n}}$ via (2, 2)-DPFs"
      assert line[618] == r"title: Homomorphic Sortition – Single Secret Leader Election for PoS Blockchains"
      assert line[619] == r"title: Hashing to elliptic curves over highly $2$-adic fields $\protect \mathbb  {F}_{\protect \!q}$ with $O(\log (q))$ operations in $\protect \mathbb  {F}_{\protect \!q}$"
      assert line[620] == r"title: More Efficient Zero-Knowledge Protocols over $\protect \mathbb  {Z}_{2^k}$ via Galois Rings"
      assert line[621] == r"title: Practical Improvement to Gaudry-Schost Algorithm on Subgroups of $\protect \mathbb  {Z}^{*}_{p}$"
      assert line[622] == r"title: Degree-$D$ Reverse Multiplication-Friendly Embeddings: Constructions and Applications"
      assert line[623] == r"title: Maravedí: A Secure and Practical Protocol to Trade Risk for Instantaneous Finality"
      assert line[624] == r"title: A simpler alternative to Lucas–Lehmer–Riesel primality test"
      assert line[625] == r"title: CNF Characterization of Sets over $\protect \mathbb  {Z}_2^n$ and Its Applications in Cryptography"
      assert line[626] == r"title: Differential Fault Attack on Rasta and $\protect \text  {FiLIP} _ {\protect \text  {DSM}}$"
      assert line[627] == r"title: The state diagram of $\chi $"
      assert line[628] == r"title: Efficient computation of $(3^n,3^n)$-isogenies"
      assert line[629] == r"title: Origami: Fold a Plonk for Ethereum’s VDF"
      assert line[630] == r"title: Batching Cipolla-Lehmer-Müller's square root algorithm with hashing to elliptic curves"
      assert line[631] == r"title: Machine-Checked Security for $\protect \mathrm  {XMSS}$ as in RFC 8391 and $\protect \mathrm  {SPHINCS}^{+}$"
      assert line[632] == r"title: Minimal $p$-ary codes from non-covering permutations"
      assert line[633] == r"title: Provable Lattice Reduction of $\protect \mathbb  Z^n$ with Blocksize $n/2$"
      assert line[634] == r"title: Batch Bootstrapping II: \\{\protect \normalsize  Bootstrapping in Polynomial Modulus Only Requires $\protect \tilde  O(1)$ FHE Multiplications in Amortization}"
      assert line[635] == r"title: End-to-End Encrypted Zoom Meetings:\\ Proving Security and Strengthening Liveness"
      assert line[636] == r"title: End-to-End Secure Messaging with Traceability\\ {\protect \em  Only} for Illegal Content"
      assert line[637] == r"title: \protect \large  {Almost Tight Multi-User Security under Adaptive Corruptions \& Leakages in the Standard Model}"
      assert line[638] == r"title: Practical Pre-Constrained Cryptography \\ \protect \Large  {(or: Balancing Privacy and Traceability in Encrypted Systems)}"
      assert line[639] == r"title: \protect \textbf  {Fully Adaptive \\Decentralized Multi-Authority \protect \textsf  {ABE}}"
      assert line[640] == r"title: On a result by Paul Erdős (a.k.a. Paul Erd\H {o}s)"

# Negative test.
# Check if we detect using "\thanks" in the author name of the \addauthor command
# --> This should fail.
def test24_test():
  path = Path('test24')
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode != 0

# Negative test.
# Check if we detect using "\thanks" in the affiliation name of the \affiliation command
# --> This should fail.
def test25_test():
  path = Path('test25')
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode != 0

# Negative test.
# Check if we detect using "\thanks" in the title \title command
# --> This should fail.
def test26_test():
  path = Path('test26')
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode != 0

# Check for writing to file in the abstract when unicode 
# characters are used.
def test27_test():
  path = Path('test27')
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      res = run_engine(option, path.iterdir(), tmpdirpath)
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

# Check for writing to file and in pdf when unicode characters are used
# in a lot of options
def test28_test():
  path = Path('test28')
  # should pass with lualatex and pdflatex
  for option in ['-pdflua', '-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode == 0
      assert 'meta' in res
      meta = meta_parse.parse_meta(res['meta'])
      assert len(meta['authors']) == 3
      assert meta['title']    == 'ÌÏÎncrëdíblé cóòömplíìîcáàäâtêd üúùûber látéx'
      assert meta['subtitle'] == 'ÌÏÎncrëdíblé cóòömplíìîcáàäâtêd üúùûber látéx'
      assert meta['authors'][0]['name'] == 'ÌÏÎncrëdíblé cóòömplíìîcáàäâtêd üúùûber látéx'
      assert meta['affiliations'][0]['name'] == 'ÌÏÎncrëdíblé cóòömplíìîcáàäâtêd üúùûber látéx'
      assert meta['affiliations'][0]['department'] == 'ÌÏÎncrëdíblé cóòömplíìîcáàäâtêd üúùûber látéx'
      assert meta['affiliations'][0]['street'] == 'ÌÏÎncrëdíblé cóòömplíìîcáàäâtêd üúùûber látéx'
      assert meta['affiliations'][0]['city'] == 'ÌÏÎncrëdíblé cóòömplíìîcáàäâtêd üúùûber látéx'
      assert meta['affiliations'][0]['state'] == 'ÌÏÎncrëdíblé cóòömplíìîcáàäâtêd üúùûber látéx'
      assert meta['affiliations'][0]['country'] == 'ÌÏÎncrëdíblé cóòömplíìîcáàäâtêd üúùûber látéx'

# Check that the log contains lines for opening and closing files.
# This will be used as the basis for a test of the latex log parser.
def test29_test():
  path = Path('test29')
  # should pass with lualatex and pdflatex
  for option in ['-pdf']:
    with tempfile.TemporaryDirectory() as tmpdirpath:
      res = run_engine(option, path.iterdir(), tmpdirpath)
      assert res['proc'].returncode == 0
      assert 'log' in res
      lines = res['log'].splitlines()
      patt = re.compile('^iacrcc:(?P<action>opened|closed) (with|as) (?P<file>.*)')
      status = {}
      opened_files = set()
      for line in lines:
        m = patt.search(line)
        if m:
          status[m.group('file')] = m.group('action')
          if m.group('action') == 'opened':
            opened_files.add(m.group('file'))
          else:
            try:
              opened_files.remove(m.group('file'))
            except Exception as e:
              # It doesn't show main.tex being opened because it is opened before
              # currfile is loaded. It still shows up as closed. This test may
              # fail unless the log file is allowed to be longer than 78 characters.
              # This is done with max_print_line=2000 in the texmf.cnf file.
              assert(m.group('file').endswith('main.tex'))
      assert len(opened_files) == 0
      assert r'Overfull \hbox' in res['log']
