"""Build an output-free, standalone notebook from percent-format Python."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def build():
    source = (ROOT / 'notebook/jagged_competence.py').read_text()
    runtime = (ROOT / 'notebook/runtime.py').read_text()
    runtime = runtime.replace('from __future__ import annotations\n', '')
    source = source.replace('from runtime import Session  # INLINE_RUNTIME', runtime)
    cells = []
    for block in re.split(r'^# %%', source, flags=re.M)[1:]:
        header, body = block.split('\n', 1)
        markdown = '[markdown]' in header
        if markdown:
            body = '\n'.join(line[2:] if line.startswith('# ') else line[1:] if line == '#' else line
                             for line in body.rstrip().splitlines())
        cell = {'cell_type': 'markdown' if markdown else 'code',
                'id': f'jagged-{len(cells):02d}', 'metadata': {}, 'source': body.rstrip() + '\n'}
        if not markdown:
            cell.update(execution_count=None, outputs=[])
            cell['metadata'] = {'cellView': 'form', 'jupyter': {'source_hidden': True}}
        cells.append(cell)
    return {'cells': cells, 'nbformat': 4, 'nbformat_minor': 5,
            'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python',
                                       'name': 'python3'},
                         'colab': {'name': 'Where Does Jagged Competence Come From?', 'provenance': []},
                         'source_sha256': hashlib.sha256(source.encode()).hexdigest()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    value = json.dumps(build(), indent=1, ensure_ascii=False) + '\n'
    target = ROOT / 'notebook/jagged_competence.ipynb'
    if args.check:
        if target.read_text() != value:
            raise SystemExit('Notebook differs from its Python sources: run python notebook/build.py')
    else:
        target.write_text(value)
    print('PASS: deterministic notebook build; outputs cleared')


if __name__ == '__main__':
    main()
