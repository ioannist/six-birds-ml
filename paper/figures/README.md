# Figure assets

Build vector PDFs with `python paper/scripts/build_figures.py`.
The builder reads only the ledger and hash-verified numerical evidence.
Each asset has a value receipt; repeated builds test byte-identical output.
PNG inspection copies are written to `paper/build/previews/`, not released
as scientific source data. Asset definitions and captions are in
`paper/scripts/figure_assets.py`; the inventory is in
`paper/notes/figure_assets.json`.
