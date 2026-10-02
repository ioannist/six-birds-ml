# arXiv source checks — 2 October 2026

This is a source-package check, not an upload or an arXiv acceptance claim.
The manuscript is copied without alteration. Bundled release metadata retains
the shared date and version but disables and omits this paper's reserved DOI.
The DOI-bearing release PDF remains unchanged by the package builder.

## Guidance checked

The official [TeX submission guide](https://info.arxiv.org/help/submit_tex.html)
and [TeX Live page](https://info.arxiv.org/help/faq/texlive.html) were checked
on 2 October 2026. They permit PDFLaTeX, PDF figures and a precompiled `.bbl`
with the main file's basename; the `.bbl` is used when supplied. They require
local dependencies and exclude unnecessary compiled/auxiliary files.

- `main.tex` is at archive root; references are `main.bbl` and `references.bib`.
- The manifest comes from a fresh main-only build's recorder. Only executed
  project inputs, the bibliography source and compiled bibliography are shipped.
- All figures use PDF and `graphicx`; no conversion, shell escape, JavaScript,
  custom class, external manuscript or absolute dependency path is needed.
- Bundled graphics have `-graphic` names and their `\includegraphics` paths are
  rewritten only inside the bundle. No PDF shares a stem with any bundled TeX
  file, so arXiv cannot discard a figure as that TeX file's compiled output.
  Every shipped graphic must appear in PDFLaTeX's final recorder input list.
- The source does not set `\pdfoutput`. PDFLaTeX's default PDF mode is used.
- `hyperref` is loaded before `cleveref`; standard `natbib`/`plainnat`, not
  `biblatex`/Biber, supplies the bibliography.
- The title date is fixed by the supplied release metadata, not `\today`.
- No manuscript PDF, supplement, build directory, log, recorder, auxiliary,
  index, PNG preview or editor backup is shipped. Figure float `.tex` files
  are real inputs, not independent documents; their PDF figures are inputs too.

## Executed check

```
python paper/scripts/build_arxiv.py
python paper/scripts/build_arxiv.py --check
```

The ZIP is extracted into a fresh temporary directory. Up to four plain
`pdflatex` passes run until labels settle, with shell escape disabled and without BibTeX. The final
log must have no undefined references/citations, no unsettled labels, and no
overfull box greater than 10 pt. Page counts must equal the DOI-bearing release
PDF. Extracted text must match exactly after Unicode NFC and whitespace
normalization except for this paper's DOI on the release title page. No other
content is omitted. Every bundled file and the compiled PDF text are checked
for this paper's identifier and the phrase "Zenodo record"; other papers' cited
DOIs remain intact.
The receipt lists every package input and SHA-256 plus archive/release hashes.
The ZIP uses fixed ordering, timestamps, modes and compression settings.

## TeX Live qualification

arXiv currently lists TeX Live 2025 (default) and 2023. The available local
installation is TeX Live 2026. All used packages belong to the standard TeX
Live distribution, and no known arXiv-specific processing issue is invoked.
An actual TeX Live 2025 compile or arXiv processing preview has **not** been
executed here; its layout is not guaranteed by the local check. The submitter
must inspect the arXiv-built preview before submission. No arXiv or Zenodo
action is taken by these scripts.
