"""Build vector figures and external PNG previews from hash-verified evidence."""
from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from asset_inputs import Inputs, ROOT
from figure_assets import FIGURES, style
from build_ledger import sha, canonical


def build(root=ROOT, preview=ROOT / 'paper/build/previews', names=None):
    ctx = Inputs(root); style(); assets = []
    for name in names or FIGURES:
        asset = FIGURES[name](ctx, preview)
        path = root / 'paper' / asset['file']
        asset['sha256'] = sha(path)
        asset['receipt_sha256'] = sha(path.with_suffix('.values.json'))
        path.with_suffix('.tex').write_text('\\begin{figure}[tb]\n\\centering\n'
            + '\\includegraphics[width=\\textwidth]{'+asset['file']+'}\n'
            + '\\caption{\\csname caption'+name+'\\endcsname}\\label{fig:'+name+'}\n\\end{figure}\n')
        asset['include_sha256'] = sha(path.with_suffix('.tex'))
        asset['preview_sha256'] = sha(preview/(name+'.png'))
        assets.append(asset)
        print(f"figure {name}: {path.stat().st_size} bytes")
    if names is None:
        ctx.assert_current()
        (root/'paper/figures/captions.tex').write_text('\n'.join(
            '\\expandafter\\def\\csname caption'+r['name']+'\\endcsname{'+r['caption']+'}' for r in assets)+'\n')
        (root/'paper/notes/figure_assets.json').write_text(canonical({'assets':assets,
            'input_policy':'ledger-bound scalar/vector or manifest-listed hash-verified file',
            'previews':'external PNG, 150 dpi; not part of the manuscript archive',
            'ledger_sha256':ctx.ledger_sha256}))
    return assets


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--preview-dir', type=Path, default=ROOT / 'paper/build/previews')
    p.add_argument('--asset', choices=sorted(FIGURES), action='append')
    p.add_argument('--verify-rebuild', action='store_true')
    a = p.parse_args(); first = build(preview=a.preview_dir, names=a.asset)
    if a.verify_rebuild:
        second = build(preview=a.preview_dir, names=a.asset)
        if first != second: raise ValueError('figure rebuild is not byte-identical')
        print('REBUILD PASS: all vector PDFs and value receipts byte-identical')
        if a.asset is None:
            (ROOT/'paper/notes/figure_reproducibility.json').write_text(canonical({
                'level':'byte-identical PDF, TeX and receipt', 'assets':len(first),
                'python':__import__('platform').python_version(),
                'matplotlib':__import__('matplotlib').__version__,
                'numpy':__import__('numpy').__version__,
                'sha256':{r['name']:r['sha256'] for r in first}}))


if __name__ == '__main__': main()
