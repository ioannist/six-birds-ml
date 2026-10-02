# Venue and format

**Target:** an arXiv preprint (cs.LG, cross-listed to cs.AI), plus a Zenodo record using the author's standard toolkit. There is no conference template. The layout is a readable single-column article, matching the corpus papers' arXiv versions in density.

**Class and preamble:** the author's glass scaffold. 11pt `article`, 1in margins, lmodern and microtype, amsmath, booktabs, natbib with `[numbers]` and `plainnat`, hyperref, cleveref and orcidlink, plus the author block and the Automorph first-page footer. No custom `.cls`. Captions are small with bold labels, and table captions go on top.

**Length:** the main text runs at most 14 pages before references. The appendix is approximately as long as the main text; the analytical supplement is at most 60 pages. Exhaustive tables are separate released data.

**Section set:**
1. Introduction, ending with a contributions list of 3–4 items.
2. Related Work, short and thematic.
3. Task and Setup: the game, A and B, strictness, and the three versions.
4. Measurements: the census, law panels, probes, swap test and controls.
5. Results, with five subsections, one per achievement.
6. Discussion.
7. Limitations, as its own numbered section.
8. Conclusion.

After the conclusion come the references and then appendices A–F.

**Figures:** 5–6 in the main text, vector PDF only, made by scripts from ledger or manifest data. Figure 1 shows the task, not a result. The appendix may hold more.

**Tables:** booktabs style. Per-seed values or ranges are given. Floors and ceilings sit in the same table.

**Citations:** numbered (natbib `numbers`, `plainnat`). Every entry with a DOI or arXiv ID carries it. Entries without identifiers are listed in the Zenodo `citation_policy`.

**arXiv source package:** self-contained. It holds `main.tex`, every transitive TeX dependency (all `\input` and `\include` files, including `includes/paper_macros.tex` and the toolkit-built `includes/release_metadata.tex`, plus any local style or class files), `references.bib` and the compiled `.bbl`, and every figure PDF. It contains no absolute paths. A packaging script lists the dependencies from a clean build and fails if any is missing. It must compile with `pdflatex` on a TeX Live version that arXiv supports. It is checked before release against the current arXiv TeX submission guidelines (https://info.arxiv.org/help/submit_tex.html). No other auxiliary build files are included beyond the `.bbl`.

**Licence on the paper:** CC BY 4.0. The licences are specified in LICENSE and LICENSE-CC-BY-4.0.
