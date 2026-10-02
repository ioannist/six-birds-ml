"""Build main, prepared and appendix TeX tables from verified study data."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asset_inputs import Inputs, ROOT
from table_assets import TABLES, SUPPLEMENT_TABLES
from build_ledger import sha, canonical


def build(root=ROOT, names=None):
    ctx = Inputs(root); assets=[]
    for name in names or TABLES:
        asset=TABLES[name](ctx)
        path=root/'paper'/asset['file']
        asset['sha256']=sha(path); asset['receipt_sha256']=sha(path.with_suffix('.values.json'))
        assets.append(asset); print(f"table {name}: {path.stat().st_size} bytes")
    if names is None:
        ctx.assert_current()
        (root/'paper/notes/table_assets.json').write_text(canonical({'assets':assets,
            'ledger_sha256':ctx.ledger_sha256,
            'display':'counts exact; other values five significant digits; unrounded receipts retained'}))
        folder=root/'paper/supplement';folder.mkdir(parents=True,exist_ok=True)
        lines=['% Built by build_tables.py; fixed supplementary table numbers.']
        for number,name in enumerate(SUPPLEMENT_TABLES,1):
            lines += [f'\\input{{tables/{name}}}']
        (folder/'table_inputs.tex').write_text('\n'.join(lines)+'\n')
        release=root/'paper/data/release'
        records=[__import__('json').loads((root/'paper'/a['file']).with_suffix('.values.json').read_text())['detailed_file']
                 for a in assets if a['name'] in SUPPLEMENT_TABLES]
        (release/'index.json').write_text(canonical({'schema':'jagged-table-release-v1','files':records}))
    return assets


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--asset', choices=sorted(TABLES), action='append')
    p.add_argument('--verify-rebuild', action='store_true')
    a=p.parse_args();first=build(names=a.asset)
    if a.verify_rebuild:
        if first != build(names=a.asset): raise ValueError('table rebuild is not byte-identical')
        print('REBUILD PASS: all TeX tables and value receipts byte-identical')
        if a.asset is None:
            (ROOT/'paper/notes/table_reproducibility.json').write_text(canonical({
                'level':'byte-identical TeX and receipt','assets':len(first),
                'sha256':{r['name']:r['sha256'] for r in first}}))


if __name__ == '__main__': main()
