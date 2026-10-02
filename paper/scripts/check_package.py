"""Compile a clean source copy and list every transitive TeX input from its recorder."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def overfull_boxes(log: str) -> list[float]:
    widths=[float(x) for x in re.findall(r'Overfull \\[hv]box \((\d+(?:\.\d+)?)pt too (?:wide|high)\)',log)]
    if any(x>10 for x in widths):
        raise ValueError(f'overfull box exceeds 10 pt: {max(widths):g} pt')
    if 'Float too large for page' in log:
        raise ValueError('figure and caption exceed the text-page height')
    return widths


def heading_only_pages(text: str) -> list[int]:
    """Refuse empty/heading-only body pages; exempt only the title page."""
    pages=text.split('\f')
    return [i for i,page in enumerate(pages,1) if i>1 and page.strip() and
            len(re.findall(r'[A-Za-z]{2,}',page))<25]


def compile_pdf(clean: Path, entry: str, job: str) -> dict:
    args=['latexmk','-pdf']+(['-jobname='+job] if job!='main' else [])+[entry]
    result=subprocess.run(args,cwd=clean,capture_output=True,text=True,timeout=600)
    if result.returncode:
        raise ValueError('clean TeX build failed:\n'+result.stdout[-9000:]+result.stderr[-2000:])
    boxes=overfull_boxes((clean/f'build/{job}.log').read_text())
    info=subprocess.check_output(['pdfinfo',str(clean/f'build/{job}.pdf')],text=True)
    pages=int(re.search(r'Pages:\s+(\d+)',info).group(1))
    result={'entrypoint':entry,'command':'cd paper && '+' '.join(args),'pages':pages,
            'pdf_bytes':(clean/f'build/{job}.pdf').stat().st_size,
            'overfull_boxes_over_10_pt':0,'maximum_overfull_pt':max(boxes,default=0)}
    if job=='supplement':
        if pages>60:raise ValueError(f'analytical supplement exceeds 60-page budget: {pages}')
        text=subprocess.check_output(['pdftotext','-layout',str(clean/f'build/{job}.pdf'),'-'],text=True)
        empty=heading_only_pages(text)
        if empty:raise ValueError(f'heading-only supplement pages: {empty}')
        result.update(page_budget=60,heading_only_pages=empty)
    if job=='main':
        aux=(clean/'build/main.aux').read_text()
        def label_page(label):
            match=re.search(r'\\newlabel\{'+label+r'\}\{\{[^}]*\}\{(\d+)\}',aux)
            return int(match.group(1)) if match else None
        end=label_page('main-text-end');start=label_page('appendix-start');last=label_page('appendix-end')
        if all(x is not None for x in (end,start,last)):
            result.update(main_text_pages=end,appendix_pages=last-start+1,references_pages=start-end-1)
    return result


def check_package(paper: Path, preview: Path | None = None) -> dict:
    dependencies = {}
    with tempfile.TemporaryDirectory(prefix="jagged-tex-", dir=os.environ.get("TMPDIR")) as scratch:
        clean = Path(scratch) / "paper"
        clean.mkdir()
        # Copy all project TeX dependencies, including referenced figures,
        # tables and local styles; never rely on a fixed directory list.
        suffixes = {".tex", ".bib", ".bst", ".sty", ".cls", ".pdf", ".png", ".jpg", ".eps"}
        for origin in paper.rglob("*"):
            relative = origin.relative_to(paper)
            if not origin.is_file() or "build" in relative.parts or "submission" in relative.parts:
                continue
            if origin.suffix not in suffixes and origin.name != "latexmkrc":
                continue
            if origin.suffix in {".tex", ".sty", ".cls"}:
                for name in re.findall(r"\\(?:input|include|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}", origin.read_text()):
                    if Path(name).is_absolute() or ".." in Path(name).parts:
                        raise ValueError(f"nonportable project dependency: {name}")
            dest = clean / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origin, dest)
        builds={'main':compile_pdf(clean,'main.tex','main')}
        if (clean/'supplement/supplement.tex').exists():
            builds['supplement']=compile_pdf(clean,'supplement/supplement.tex','supplement')
        previews=[]
        if preview is not None:
            preview.mkdir(parents=True,exist_ok=True)
            for job,labels in (('main',('table1','table2')),('supplement',('table1_full','appendix_C_calibration','appendix_E_r12_probes'))):
                if job not in builds:continue
                aux=(clean/f'build/{job}.aux').read_text()
                for label in labels:
                    match=re.search(r'\\newlabel\{tab:'+label+r'\}\{\{[^}]*\}\{(\d+)\}',aux)
                    if not match:raise ValueError(f'typeset table lacks a page reference: {label}')
                    page=match.group(1);name=f'{job}_{label}_page{page}'
                    subprocess.run(['pdftoppm','-f',page,'-l',page,'-r','150','-singlefile','-png',
                        str(clean/f'build/{job}.pdf'),str(preview/name)],check=True,timeout=60,
                        capture_output=True)
                    previews.append({'file':name+'.png','page':int(page),'pdf':job,
                        'sha256':hashlib.sha256((preview/(name+'.png')).read_bytes()).hexdigest()})
        for line in [line for job in builds for line in (clean/f'build/{job}.fls').read_text().splitlines()]:
            if not line.startswith("INPUT "):
                continue
            path = Path(line[6:])
            if not path.is_absolute():
                path = clean / path
            path = path.resolve()
            if not path.is_file():
                raise ValueError(f"missing recorded input: {path}")
            if path.is_relative_to(clean):
                name = path.relative_to(clean).as_posix()
                kind = "build_product" if name.startswith("build/") else "project_source"
            else:
                # Distribution inputs, never a private sibling manuscript.
                if path.name == "texmf.cnf" and ".TinyTeX" in path.parts:
                    name = "TeX_distribution/texmf.cnf"
                    kind = "TeX_distribution"
                    dependencies[name] = {"path": name, "kind": kind,
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                    continue
                if not any(x in path.parts for x in ("texmf-dist", "texmf-var", "texmf-config")):
                    raise ValueError(f"nonportable external TeX dependency: {path}")
                index = next(i for i, x in enumerate(path.parts) if x.startswith("texmf-"))
                name = "/".join(path.parts[index:])
                kind = "TeX_distribution"
            dependencies[name] = {"path": name, "kind": kind,
                                  "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        # BibTeX inputs do not all occur in pdflatex's .fls.
        for name in ("references.bib", "latexmkrc"):
            dependencies[name] = {"path": name, "kind": "project_source",
                                  "sha256": hashlib.sha256((clean / name).read_bytes()).hexdigest()}
        for name in ("plainnat.bst",):
            path = subprocess.check_output(["kpsewhich", name], text=True).strip()
            if path and Path(path).is_file():
                dependencies[name] = {"path": name, "kind": "TeX_distribution",
                    "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()}
        version = subprocess.check_output(["latexmk", "-v"], text=True).strip()
        return {"clean_location_build": "PASS", "command": "cd paper && latexmk -pdf main.tex",
                "latexmk_version": version, "dependencies": sorted(dependencies.values(), key=lambda x: x["path"]),
                "pdf_bytes": (clean / "build/main.pdf").stat().st_size,
                "pdfs":builds,
                "typeset_table_previews":previews,
                "licence_status": "MIT code / CC BY 4.0 paper, figures and released data; manuscript release identity comes from includes/release_metadata.tex"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preview-dir", type=Path, help="external 150-dpi typeset table inspection copies")
    args = parser.parse_args()
    result = check_package(args.paper.resolve(),args.preview_dir)
    content = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(content)
    else:
        print(content)


if __name__ == "__main__":
    main()
