# Submission artifacts

**Where Does Jagged Competence Come From?** — Preprint v1.0.
The DOI **10.5281/zenodo.23094485** is reserved but unpublished. These files
constitute a draft, not a published deposit.

## Inventory

- `artifacts/Tsiokos_2026_Where_Does_Jagged_Competence_Come_From.pdf`: the DOI-bearing main paper.
- `artifacts/Tsiokos_2026_Where_Does_Jagged_Competence_Come_From_Supplement.pdf`: the accompanying analytical supplement.
- `build_arxiv.py` in `paper/scripts/` builds a self-contained main-paper source package. The distribution does not include source archives. The supplement is separate. The source package omits this paper's reserved DOI, while retaining the identifiers of cited works. The submitted PDF above retains its DOI.
- `arxiv_package_receipt.json` and `ARXIV_CHECKS.md`: source inventory, hashes and compilation checks.
- `zenodo-metadata.json` and `zenodo-description.html`: the deposit metadata and description.
- `zenodo-config.json`: the deposit configuration.
- `zenodo-release.json`: the local release record, including artifact and metadata identities.

## Verification

Run from the repository root. Submitted PDFs are immutable historical artifacts;
clean-source compilation is checked separately.

```sh
python paper/scripts/check_package.py
python paper/scripts/build_ledger.py --check --verify-all
```
