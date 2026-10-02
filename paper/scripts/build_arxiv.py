"""Build and check the manuscript-only arXiv source archive, without uploads."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata
import zipfile

from check_package import compile_pdf, overfull_boxes

PAPER = Path(__file__).resolve().parents[1]
RELEASE_NAME = 'Tsiokos_2026_Where_Does_Jagged_Competence_Come_From'
ALLOWED = {'.tex', '.bib', '.bbl', '.pdf', '.sty', '.cls', '.bst'}
PAPER_DOI = '10.5281/zenodo.23094485'
FORBIDDEN = ('zenodo.23094485', 'Zenodo record')


def verify_identifier_text(text, name):
    for token in FORBIDDEN:
        if token.lower() in text.lower():
            raise ValueError(f'paper identifier forbidden in arXiv input: {name}: {token}')


def arxiv_metadata(text):
    """Suppress this paper's reserved DOI in the bundled metadata only."""
    if text.count(r'\paperhasdoitrue') != 1:
        raise ValueError('release metadata must declare exactly one DOI-bearing identity')
    text = text.replace(r'\paperhasdoitrue', r'\paperhasdoifalse')
    text, count = re.subn(r'(?m)^\\newcommand\{\\paperdoi\}\{[^\n}]*\}\n?', '', text)
    if count != 1:
        raise ValueError('release metadata must define exactly one paper DOI')
    verify_identifier_text(text, 'includes/release_metadata.tex')
    return text


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graphic_names(files):
    """Bundle-only names; avoid TeX stems globally, not merely in one folder."""
    forbidden = {Path(name).stem for name in files if Path(name).suffix in {'.tex', '.pdf'}}
    renamed = {}
    for name in sorted(files):
        path = Path(name)
        if path.suffix != '.pdf':
            continue
        stem, count = path.stem + '-graphic', 1
        while stem in forbidden:
            count += 1
            stem = path.stem + f'-graphic-{count}'
        forbidden.add(stem)
        renamed[name] = path.with_name(stem + '.pdf').as_posix()
    return renamed


def rewrite_graphics(text, renamed):
    def replace(match):
        name = Path(match.group(2)).as_posix()
        original = name if Path(name).suffix else name + '.pdf'
        return match.group(1) + renamed.get(original, match.group(2)) + '}'
    return re.sub(r'(\\includegraphics\*?(?:\[[^\]]*\])?\{)([^}]+)\}', replace, text)


def validate_tree(folder):
    files = sorted(p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file())
    if 'main.pdf' in files:
        raise ValueError('compiled manuscript must not be in source package')
    tex_stems = {Path(name).stem for name in files if Path(name).suffix == '.tex'}
    for name in files:
        if Path(name).suffix == '.pdf' and Path(name).stem in tex_stems:
            raise ValueError(f'PDF/TeX stem conflict: {name}')
    for name in files:
        path = folder / name
        if name == 'main.pdf':
            raise ValueError('compiled manuscript must not be in source package')
        if path.is_symlink() or path.suffix not in ALLOWED or 'supplement' in path.relative_to(folder).parts:
            raise ValueError(f'extraneous arXiv input: {name}')
        if path.suffix == '.bbl' and name != 'main.bbl':
            raise ValueError(f'extraneous bibliography: {name}')
        verify_identifier_text(path.read_bytes().decode('latin1'), name)
        if path.suffix == '.pdf':
            verify_identifier_text(normalized_text(path), name)
        if path.suffix in {'.tex', '.sty', '.cls', '.bst', '.bib', '.bbl'}:
            text = path.read_text()
            if re.search(r'/(?:home|mnt|tmp|usr|opt)/', text):
                raise ValueError(f'absolute private/system path: {name}')
            for value in re.findall(r'\\(?:input|include|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}', text):
                if Path(value).is_absolute() or '..' in Path(value).parts:
                    raise ValueError(f'nonportable dependency: {name}: {value}')
            if re.search(r'\\(?:write18|pdfoutput)\b|\\usepackage(?:\[[^\]]*\])?\{(?:minted|psfig)\}', text):
                raise ValueError(f'unsupported processing directive: {name}')
    if not {'main.tex', 'main.bbl', 'references.bib'} <= set(files):
        raise ValueError('main.tex, main.bbl and references.bib are required')
    return files


def normalized_text(pdf):
    text = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text)).strip()


def pages(pdf):
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
    return int(re.search(r'Pages:\s+(\d+)', info).group(1))


def isolated_tex_environment():
    return {k: v for k, v in os.environ.items()
            if k not in {'TEXINPUTS', 'BIBINPUTS', 'BSTINPUTS', 'TEXMFHOME'}}


def verify_archive(archive, release):
    """Extract, then run plain pdflatex until labels settle (at most four passes); never run BibTeX."""
    with tempfile.TemporaryDirectory(prefix='jagged-arxiv-', dir=os.environ.get('TMPDIR')) as scratch:
        clean = Path(scratch)
        with zipfile.ZipFile(archive) as bundle:
            names = []
            for member in bundle.infolist():
                name = member.filename
                if (member.is_dir() or Path(name).is_absolute() or '..' in Path(name).parts
                        or '\\' in name or (member.external_attr >> 16) & 0o170000 == 0o120000):
                    raise ValueError(f'unsafe archive member: {name}')
                names.append(name)
            if len(names) != len(set(names)):
                raise ValueError('duplicate archive member')
            bundle.extractall(clean)
        contents = validate_tree(clean)
        args = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
                '-file-line-error', '-recorder', 'main.tex']
        # arXiv's compiler reruns pdflatex until labels settle; allow up to four passes.
        unsettled = r'(?:Reference|Citation).*undefined|undefined (?:references|citations)|Label\(s\) may have changed'
        for executed_passes in range(1, 5):
            result = subprocess.run(args, cwd=clean, capture_output=True, text=True, timeout=180,
                                    env=isolated_tex_environment())
            if result.returncode:
                raise ValueError('plain pdflatex failed:\n' + result.stdout[-6000:] + result.stderr[-2000:])
            log = (clean / 'main.log').read_text()
            if not re.search(unsettled, log):
                break
        else:
            raise ValueError('references/citations did not settle after four passes')
        boxes = overfull_boxes(log)
        graphics = sorted(name for name in contents if Path(name).suffix == '.pdf')
        consumed = set()
        for line in (clean / 'main.fls').read_text().splitlines():
            if line.startswith('INPUT '):
                path = Path(line[6:])
                path = (path if path.is_absolute() else clean / path).resolve()
                if path.is_relative_to(clean):
                    consumed.add(path.relative_to(clean).as_posix())
        missing = set(graphics) - consumed
        if missing:
            raise ValueError(f'bundled graphics not included by pdflatex: {sorted(missing)}')
        produced = clean / 'main.pdf'
        actual, expected = normalized_text(produced), normalized_text(release)
        verify_identifier_text(actual, 'compiled arXiv PDF text')
        # Remove only the release title-page DOI, never a cited work's DOI.
        first_page = subprocess.check_output(
            ['pdftotext', '-f', '1', '-l', '1', '-layout', str(release), '-'], text=True)
        title_doi = 'DOI: ' + PAPER_DOI
        if title_doi not in re.sub(r'\s+', ' ', first_page) or expected.count(title_doi) != 1:
            raise ValueError('release must contain this paper DOI exactly once, on the title page')
        expected = re.sub(r'\s+', ' ', expected.replace(title_doi, '', 1)).strip()
        if pages(produced) != pages(release):
            raise ValueError(f'page count differs: {pages(produced)} versus release {pages(release)}')
        if actual != expected:
            diff = '\n'.join(difflib.unified_diff(expected.split(' '), actual.split(' '),
                            fromfile='release', tofile='arxiv', n=3))
            raise ValueError('extracted PDF text differs (whitespace normalized):\n' + diff[:6000])
        for name in contents:
            if Path(name).suffix == '.pdf':
                info = subprocess.check_output(['pdfinfo', str(clean / name)], text=True)
                if not re.search(r'JavaScript:\s+no', info):
                    raise ValueError(f'figure JavaScript status is not explicitly no: {name}')
        return {'result': 'PASS', 'passes': executed_passes, 'command': ' '.join(args), 'bibtex_invocations': 0,
                'pages': pages(produced), 'release_pages': pages(release),
                'text_match': 'exact after NFC and whitespace normalization except the release title-page DOI',
                'paper_identifier_check': 'PASS: absent from every bundled file and compiled PDF text',
                'text_sha256': hashlib.sha256(actual.encode()).hexdigest(),
                'undefined_references': 0, 'undefined_citations': 0,
                'figure_javascript': 'none; every shipped figure checked with pdfinfo',
                'graphic_stem_check': 'PASS: no PDF shares a stem with any bundled TeX file',
                'included_graphics': graphics,
                'maximum_overfull_pt': max(boxes, default=0), 'files': contents,
                'pdflatex_version': subprocess.check_output(['pdflatex', '--version'], text=True).splitlines()[0]}


def write_archive(folder, destination):
    files = validate_tree(folder)
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name in files:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, (folder / name).read_bytes(), compresslevel=9)


def build(paper=PAPER):
    release = paper / 'submission/artifacts' / (RELEASE_NAME + '.pdf')
    release_hash = sha(release)
    with tempfile.TemporaryDirectory(prefix='jagged-arxiv-source-', dir=os.environ.get('TMPDIR')) as scratch:
        clean = Path(scratch)
        # A fresh main-only build supplies the recorder and matching .bbl.
        for origin in paper.rglob('*'):
            relative = origin.relative_to(paper)
            if origin.is_file() and not {'build', 'submission', 'supplement'} & set(relative.parts) and origin.suffix in ALLOWED - {'.bbl'}:
                dest = clean / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(origin, dest)
        shutil.copyfile(paper / 'latexmkrc', clean / 'latexmkrc')
        compile_pdf(clean, 'main.tex', 'main')
        selected = {'references.bib'}
        distribution = set()
        for line in (clean / 'build/main.fls').read_text().splitlines():
            if not line.startswith('INPUT '):
                continue
            path = Path(line[6:])
            path = (path if path.is_absolute() else clean / path).resolve()
            if path.is_relative_to(clean) and path.is_file():
                relative = path.relative_to(clean)
                if 'build' not in relative.parts:
                    selected.add(relative.as_posix())
            elif path.is_file() and path.suffix in {'.sty', '.cls', '.tex', '.def', '.fd'}:
                if not any(part in {'texmf-dist', 'texmf-var', 'texmf-config'} for part in path.parts):
                    raise ValueError(f'external non-distribution TeX input: {path}')
                distribution.add(path.name)
        folder = paper / 'submission/arxiv'
        folder.mkdir(parents=True, exist_ok=True)
        renamed = graphic_names(selected)
        extras = ({p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
                  - selected - set(renamed.values()) - {'main.bbl'})
        if extras:
            raise ValueError(f'preserved unexpected existing package files; remove explicitly: {sorted(extras)}')
        for name in sorted(selected):
            dest = folder / renamed.get(name, name)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if Path(name).suffix == '.tex':
                text = (clean / name).read_text()
                if name == 'includes/release_metadata.tex':
                    text = arxiv_metadata(text)
                dest.write_text(rewrite_graphics(text, renamed))
            else:
                shutil.copyfile(clean / name, dest)
        # Remove only superseded bundle copies, never the original source assets.
        for name in renamed:
            obsolete = folder / name
            if obsolete.is_file():
                if sha(obsolete) != sha(clean / name):
                    raise ValueError(f'cannot remove modified legacy bundle graphic: {name}')
                obsolete.unlink()
        shutil.copyfile(clean / 'build/main.bbl', folder / 'main.bbl')
    archive = paper / 'submission/arxiv_source.zip'
    write_archive(folder, archive)
    verification = verify_archive(archive, release)
    if sha(release) != release_hash:
        raise ValueError('release PDF changed during verification')
    sources = {renamed.get(name, name): name for name in selected}
    receipt = {'schema': 'jagged-arxiv-source-v3', 'archive': 'arxiv_source.zip',
               'archive_sha256': sha(archive), 'archive_bytes': archive.stat().st_size,
               'release': 'artifacts/' + release.name, 'release_sha256': release_hash,
               'files': [{'path': name, 'sha256': sha(folder / name), 'bytes': (folder / name).stat().st_size,
                          'source_path': sources.get(name, name)}
                         for name in verification.pop('files')], 'verification': verification,
               'tex_distribution_inputs': sorted(distribution),
               'guidelines': 'ARXIV_CHECKS.md', 'no_supplement': True,
               'graphic_renames': renamed}
    (paper / 'submission/arxiv_package_receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'files': len(receipt['files']), 'archive_bytes': receipt['archive_bytes'],
                      'verification': verification}, indent=2))
    return receipt


def check(paper=PAPER):
    receipt = json.loads((paper / 'submission/arxiv_package_receipt.json').read_text())
    archive = paper / 'submission' / receipt['archive']
    if sha(archive) != receipt['archive_sha256']:
        raise ValueError('archive hash differs')
    folder = paper / 'submission/arxiv'
    source_files = {row['source_path'] for row in receipt['files'] if row['path'] != 'main.bbl'}
    renamed = graphic_names(source_files)
    if renamed != receipt['graphic_renames']:
        raise ValueError('graphic name transformation differs from recorded sources')
    if validate_tree(folder) != [row['path'] for row in receipt['files']]:
        raise ValueError('package file set differs')
    for row in receipt['files']:
        if sha(folder / row['path']) != row['sha256']:
            raise ValueError(f'package input hash differs: {row["path"]}')
        if row['path'] != 'main.bbl':
            source = paper / row['source_path']
            if source.suffix == '.tex':
                text = source.read_text()
                if row['source_path'] == 'includes/release_metadata.tex':
                    text = arxiv_metadata(text)
                if (folder / row['path']).read_text() != rewrite_graphics(text, renamed):
                    raise ValueError(f'package TeX transformation differs from current source: {row["path"]}')
            elif sha(source) != row['sha256']:
                raise ValueError(f'package differs from current source: {row["path"]}')
    release = paper / 'submission' / receipt['release']
    if sha(release) != receipt['release_sha256']:
        raise ValueError('release PDF hash differs')
    return verify_archive(archive, release)


def public_source(paper=PAPER, checking=False):
    """Check portable sources independently of immutable submitted PDFs.

    The archive is a local build product, not part of the source distribution.
    Its reference PDF comes from the same clean portable sources; the original
    submitted artifacts are never changed or claimed byte-identical.
    """
    clean = paper / 'build/arxiv_reproduction'
    if checking:
        return check(clean)
    clean.mkdir(parents=True, exist_ok=True)
    for origin in paper.rglob('*'):
        relative = origin.relative_to(paper)
        if not origin.is_file() or {'build', 'submission'} & set(relative.parts):
            continue
        if origin.suffix not in ALLOWED or origin.suffix == '.bbl':
            continue
        target = clean / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin, target)
    shutil.copyfile(paper / 'latexmkrc', clean / 'latexmkrc')
    compile_pdf(clean, 'main.tex', 'main')
    submitted = clean / 'submission/artifacts' / (RELEASE_NAME + '.pdf')
    submitted.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(clean / 'build/main.pdf', submitted)
    return build(clean)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--public-source', action='store_true',
                        help='use a clean portable-source PDF as the reference; retain submitted PDFs unchanged')
    args = parser.parse_args()
    if args.public_source:
        print(json.dumps(public_source(checking=args.check), indent=2))
    else:
        print(json.dumps(check(), indent=2)) if args.check else build()
