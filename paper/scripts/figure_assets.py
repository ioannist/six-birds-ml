"""One callable entry point per vector asset; no neural computation or fitting."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR',str(Path(os.environ.get('TMPDIR','/tmp'))/'jagged-paper-matplotlib'))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from condition_labels import condition_name

PALETTE = {"records": "#0072B2", "supplied": "#009E73", "sums": "#D55E00",
           "frozen": "#CC79A7", "live": "#E69F00", "numerical": "#56B4E9",
           "adam": "#009E73", "reduced": "#CC79A7", "sgd": "#56B4E9", "blocked": "#595959"}
MARKERS = ["o", "s", "^"]
LABELS = {"records": r"records $\to$ prediction", "supplied": r"records+sums $\to$ prediction",
          "sums": r"records $\to$ prediction+sums", "adam": "AdamW", "reduced": "reduced-lr AdamW",
          "sgd": "SGD", "blocked": "blocked prediction gradient"}


def style():
    # The document's Latin Modern font includes the en dash and arrow. Inequality
    # glyphs use CM math, not the text font's unrelated ASCII ligatures.
    font = subprocess.check_output(["kpsewhich", "lmroman10-regular.otf"], text=True).strip()
    if not font:
        raise ValueError("Latin Modern Roman is required for manuscript figures")
    font_manager.fontManager.addfont(font)
    plt.rcParams.update({"font.family": "serif", "font.serif": ["Latin Modern Roman"], "font.size": 8,
        "mathtext.fontset": "cm", "axes.formatter.use_mathtext": False, "axes.unicode_minus": False,
        "axes.titlesize": 9, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "legend.fontsize": 7, "pdf.fonttype": 42, "ps.fonttype": 42,
        "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.2})


def ceiling(ax, value=0, label="exact oracle"):
    ax.axhline(value, color="black", lw=.8, ls="--", label=label, zorder=1)


def require_series(values, name):
    if not values:
        raise ValueError(f"empty measured series: {name}")
    return values


def natural_support(ctx):
    """Read the already pinned panel-size declarations; no sampler is run."""
    import ast
    entry=ctx.evidence.entries['repo/src/recombination_promotion/oldgame_ext/multiround.py']
    ctx.evidence.verify(entry)
    ctx.receipts.append({'source':entry['id'],'pointer':[],'sha256':entry['sha256'],'manifest_only':True,'non_json':True})
    tree=ast.parse(ctx.evidence.path(entry).read_text())
    sizes=next(ast.literal_eval(node.value) for node in tree.body if isinstance(node,ast.Assign)
               and isinstance(node.targets[0],ast.Tuple) and
               [n.id for n in node.targets[0].elts]==['TEST_EPISODES','TEST_ROUNDS'])
    if sizes!=(5000,12):raise ValueError('natural panel support differs from manuscript declaration')
    return sizes


def panel_letters(fig):
    """Letter before final layout, so titles participate in its calculation."""
    for index, ax in enumerate(fig.axes):
        if len(fig.axes) > 1 and not getattr(ax, '_paper_lettered', False):
            title = ax.get_title()
            ax.set_title('', loc='center')
            ax.set_title(f"({chr(97+index)}) {title}", loc='left',
                         pad=getattr(ax, '_paper_title_pad', 10))
            ax._paper_lettered = True


def text_in_canvas(fig, renderer):
    canvas = fig.bbox
    for text in fig.findobj(matplotlib.text.Text):
        if not text.get_visible() or not text.get_text():
            continue
        # Ignore tick labels outside the axis view interval (log locators keep
        # dormant ticks in the artist tree).
        if (text in fig.texts or not text.get_clip_on()) and text.get_in_layout():
            b = text.get_window_extent(renderer)
            if b.x0 < canvas.x0-1 or b.y0 < canvas.y0-1 or b.x1 > canvas.x1+1 or b.y1 > canvas.y1+1:
                raise ValueError(f"text outside canvas: {text.get_text()}")
    for ax in fig.axes:
        b=ax.get_tightbbox(renderer)
        if b is not None and (b.x0<canvas.x0-1 or b.y0<canvas.y0-1 or b.x1>canvas.x1+1 or b.y1>canvas.y1+1):
            raise ValueError(f'text outside canvas: axis labels or panel title ({ax._left_title.get_text()}, bounds={b.bounds}, canvas={canvas.bounds})')


def save(ctx, name, fig, caption, preview, *, task_checks=None):
    folder = ctx.root / "paper/figures"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.pdf"
    # Plain exponent notation keeps log-axis superscripts from becoming
    # smaller than the declared 7-pt minimum at manuscript print size.
    for ax in fig.axes:
        if ax.get_yscale()!='linear':ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x:g}'))
    panel_letters(fig)
    panels = [chr(97+i) for i in range(len(fig.axes))] if len(fig.axes)>1 else []
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    if any(ax.get_legend() is not None for ax in fig.axes):
        raise ValueError('figure legends must be shared and outside data axes')
    for legend in fig.legends:
        bounds = legend.get_window_extent(renderer)
        if any(bounds.overlaps(ax.get_window_extent(renderer)) or
               bounds.overlaps(ax._left_title.get_window_extent(renderer)) for ax in fig.axes):
            raise ValueError('shared legend overlaps a data axis or panel title')
    # A title added after layout must not collide with a neighbouring panel's
    # axis label (especially when panels span different numbers of grid rows).
    panel_texts = []
    for ax in fig.axes:
        ticks = []
        for axis, limits in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
            low, high = sorted(limits)
            ticks.extend(tick.label1 for tick in axis.get_major_ticks()
                         if low <= tick.get_loc() <= high)
        panel_texts.append([t for t in [ax._left_title, ax.title, ax.xaxis.label,
                           ax.yaxis.label, *ax.texts, *ticks] if t.get_visible() and t.get_text()])
    for i, texts in enumerate(panel_texts):
        for other in panel_texts[i+1:]:
            for a in texts:
                for b in other:
                    if a.get_window_extent(renderer).overlaps(b.get_window_extent(renderer)):
                        raise ValueError(f'text overlaps across figure panels: {a.get_text()} / {b.get_text()}')
    text_in_canvas(fig, renderer)
    fig.savefig(path, metadata={"CreationDate": None, "ModDate": None,
                                "Creator": "paper/scripts/build_figures.py"})
    preview.mkdir(parents=True, exist_ok=True)
    fig.savefig(preview / f"{name}.png", dpi=150)
    if name == 'fig1':
        fig.savefig(preview / 'fig1_layers.png', dpi=200)
    fonts = [t.get_fontsize() for t in fig.findobj(matplotlib.text.Text)]
    if min(fonts, default=8) < 7:
        raise ValueError("figure contains text smaller than 7 pt")
    plt.close(fig)
    ctx.save_receipts(name, "figures", caption, {"width_inches": 6.5, "height_inches": float(fig.get_size_inches()[1]),
                     "minimum_font_pt": min(fonts, default=8),
                     "matplotlib": matplotlib.__version__, "numpy": np.__version__,
                     "font": "Latin Modern Roman / CM math; embedded vector text",
                     "panel_letters": panels,
                     "legend_outside_axes": True,
                     "panel_text_disjoint": True,
                     "text_in_canvas": True,
                     "palette": PALETTE, "preview_dpi": 150,
                     **({'task_checks': task_checks, 'additional_preview_dpi': 200}
                        if task_checks is not None else {})})
    return {"name": name, "file": str(path.relative_to(ctx.root / "paper")), "caption": caption}


def box(ax, x, y, w, h, text, color="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006", fc=color, ec="#444444", lw=.8))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=8)


def arrow(ax, a, b, **kw):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=10, lw=.8, color="#444444", **kw))


def shared_legend(fig, axes, *, y=.01, ncol=3):
    """Place a deduplicated figure legend in reserved, non-data space."""
    items = {}
    for ax in np.asarray(axes).flat:
        handles, labels = ax.get_legend_handles_labels()
        for handle, label in zip(handles, labels):
            items.setdefault(label, handle)
    return fig.legend(items.values(), items, loc='lower center',
                      bbox_to_anchor=(.5, y), ncol=ncol, frameon=False)


def fig1_mass_vocabulary(source):
    """Read exact declarations without importing unrelated corpus machinery.

    The caller verifies the source hash. This deliberately narrow AST reader
    also works in the public evidence subset, which is not a training install.
    """
    import ast
    from fractions import Fraction
    declarations = {}
    for node in ast.parse(source.read_text()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            declarations[node.targets[0].id] = node.value
    tokens = ast.literal_eval(declarations['DEFAULT_MASS_VOCAB'])
    values = declarations['MASS_VALUE']
    if not isinstance(values, ast.Dict):
        raise ValueError('mass declarations are not the registered exact rational form')
    masses = {}
    for key, value in zip(values.keys, values.values, strict=True):
        if not (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
                and value.func.id == 'Fraction' and len(value.args) == 2 and not value.keywords):
            raise ValueError('mass declarations are not the registered exact rational form')
        masses[ast.literal_eval(key)] = Fraction(*(ast.literal_eval(arg) for arg in value.args))
    twelfths = tuple(12 * masses[token] for token in tokens)
    if any(m.denominator != 1 for m in twelfths):
        raise ValueError('registered mass is not an integer twelfth')
    return tuple(int(m) for m in twelfths)


def fig1_witness_records(task, witness, mass_source=None):
    """Check the specified witness using the exact Stage-1 mass declarations.

    These legal renderings are task examples, not the older ledger witness's
    particular prefix boards. Only its registered laws are reused.
    """
    if mass_source is None:
        mass_source = Path(__file__).resolve().parents[2] / 'src/recombination_promotion/serialization/minimal_recombination.py'
    masses_vocab = fig1_mass_vocabulary(mass_source)
    records = {8: [2, 2, 2, 2], 13: [2, 3, 4, 4], 36: [9, 9, 9, 9]}
    if (task['records'], task['slots'], task['boards'], task['histories']) != (4, 5, 24435, 1555):
        raise ValueError('two-layer task support differs')
    for total, masses in records.items():
        if len(masses) != task['records'] or not all(m in masses_vocab for m in masses) or sum(masses) != total:
            raise ValueError('witness board has no declared legal four-record rendering')
    if witness['off_law'] != task['p0'] or witness['on_law'] != task['p1']:
        raise ValueError('witness laws differ from the task')
    if task['p0'] != [.5, .25, .25] or task['p1'] != [.25, .25, .5]:
        raise ValueError('two-layer exact laws differ')
    return [{'board': [total, 0, 0, 0, 0], 'records': [[0, m] for m in masses],
             'category': 'L' if total <= 12 else 'H' if total >= 24 else 'N'}
            for total, masses in records.items()]


def fig1(ctx, preview):
    ctx.begin()
    task = ctx.ref('quantities', 'task')
    witness = ctx.ref('quantities', 'theory_nonfactorization')
    mass_source = None
    for source in ('oldgame_ext/game.py', 'serialization/minimal_recombination.py'):
        entry = ctx.evidence.entries['repo/src/recombination_promotion/' + source]
        ctx.evidence.verify(entry)
        ctx.receipts.append({'source': entry['id'], 'pointer': [], 'sha256': entry['sha256'],
                             'manifest_only': True, 'non_json': True})
        if source.startswith('serialization/'):
            mass_source = ctx.evidence.path(entry)
    checks = fig1_witness_records(task, witness, mass_source)
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.3),
                             gridspec_kw={'width_ratios': [2.05, 1]})
    for ax, width in zip(axes, (4.05, 4.30), strict=True):
        ax.set(xlim=(0, width), ylim=(0, 3.12)); ax.axis('off')
        ax._paper_title_pad = 8
    ax = axes[0]; ax.set_title('Exact task construction')
    # Band backgrounds separate two task computations, not neural modules.
    for y, h, color in ((1.94, 1.16, '#fff5eb'), (.95, .74, '#eef5fa')):
        ax.add_patch(FancyBboxPatch((.02, y), 3.98, h, boxstyle='round,pad=0.01',
                                   fc=color, ec='none'))
    ax.text(.13, 3.02, 'Layer B: computation across rounds', va='center', fontsize=9)
    ax.text(1.08, 2.90, 'L: off · H: on · N: unchanged', ha='center', va='top', fontsize=7)
    box(ax, .13, 2.00, 1.10, .36, '')
    ax.patches[-1].set_gid('fig1_category')
    ax.text(.68, 2.28, 'slot-1 category', ha='center', fontsize=8)
    ax.text(.68, 2.15, r'L: $s\leq12$ · H: $s\geq24$', ha='center', fontsize=7)
    ax.text(.68, 2.04, 'N: 13–23', ha='center', fontsize=7)
    box(ax, .13, 2.44, 1.10, .22, 'previous mode')
    ax.patches[-1].set_gid('fig1_previous_mode')
    box(ax, 1.62, 2.22, .90, .32, 'updated mode')
    ax.patches[-1].set_gid('fig1_updated_mode')
    arrow(ax, (1.25, 2.55), (1.60, 2.45))
    ax.patches[-1].set_gid('fig1_previous_to_updated')
    arrow(ax, (1.25, 2.18), (1.60, 2.31))
    ax.patches[-1].set_gid('fig1_category_to_updated')
    box(ax, 2.82, 2.02, 1.17, .70, '')
    ax.patches[-1].set_gid('fig1_law_block')
    arrow(ax, (2.54, 2.38), (2.80, 2.38))
    ax.patches[-1].set_gid('fig1_updated_to_law')
    ax.text(3.405, 2.55, 'next-category law\nover (L, N, H)', ha='center', va='center', fontsize=8)
    ax.text(3.405, 2.29, 'off: (1/2, 1/4, 1/4)', ha='center', color=PALETTE['records'], fontsize=8)
    ax.text(3.405, 2.10, 'on: (1/4, 1/4, 1/2)', ha='center', color=PALETTE['sums'], fontsize=8)
    # The feedback has its own lane above the boxes and below the subtitle.
    from matplotlib.path import Path as PlotPath
    feedback = [(2.07, 2.546), (2.07, 2.76), (.68, 2.76), (.68, 2.667)]
    loop = FancyArrowPatch(path=PlotPath(feedback,
        [PlotPath.MOVETO, *[PlotPath.LINETO]*3]), arrowstyle='-|>',
        mutation_scale=9, lw=.8, color='#444444')
    loop.set_gid('fig1_mode_feedback'); loop._paper_vertices = feedback
    ax.add_patch(loop)
    ax.text(1.28, 2.70, 'next round', ha='left', va='top', fontsize=7)
    # Indent the one-line title to leave the category's vertical lane clear.
    ax.text(1.03, 1.57, 'Layer A: current-round computation', va='center', fontsize=9)
    box(ax, 2.21, 1.04, 1.78, .34, 'Four records in slot 1\nmasses 2, 3, 4, 4 (twelfths)')
    arrow(ax, (2.19, 1.18), (2.03, 1.18))
    ax.text(1.43, 1.355, 'five per-slot sums', ha='center', fontsize=8)
    for j, value in enumerate(checks[1]['board']):
        box(ax, .55+j*.30, 1.03, .26, .25, str(value), '#ddeef8' if j == 0 else '#ffffff')
        if j == 0:
            ax.patches[-1].set_edgecolor(PALETTE['records'])
            ax.patches[-1].set_linewidth(1.2)
            ax.patches[-1].set_gid('fig1_slot1_sum')
    category_connection = [(.68, 1.286), (.68, 1.994)]
    link = FancyArrowPatch(path=PlotPath(category_connection,
        [PlotPath.MOVETO, PlotPath.LINETO]), arrowstyle='-|>', mutation_scale=10,
        lw=1.0, color=PALETTE['records'])
    link.set_gid('fig1_a_to_b'); link._paper_vertices = category_connection
    ax.add_patch(link)
    ax.text(.78, 1.83, 'B consumes the\nslot-1 category', ha='left', va='center',
            color=PALETTE['records'], fontsize=8)
    # Deliberately no graph edges join this strip to either task band.
    ax.add_patch(FancyBboxPatch((.02, .015), 3.98, .77, boxstyle='round,pad=0.01',
                               fc='#f5f5f5', ec='#bbbbbb', lw=.6))
    ax.text(.13, .65, 'Availability of A during training', fontsize=8)
    for y, text in ((.47, 'Prediction loss only: A not supervised or supplied.'),
                    (.28, 'Exact sums supplied: A available as input.'),
                    (.09, 'Sums also supervised: output disconnected / connected.')):
        ax.text(.13, y, text, fontsize=8)
    ax = axes[1]; ax.set_title('Same sums, different laws')
    ax.text(2.15, 2.98, 'Both start with mode off', ha='center', fontsize=8)
    for y, initial, law, color in ((2.45, 8, '(1/2,1/4,1/4)', PALETTE['records']),
                                   (1.20, 36, '(1/4,1/4,1/2)', PALETTE['sums'])):
        # Wrap, rather than shrink, the board vectors in the narrow inset.
        box(ax, .03, y-.27, .85, .54, f"{'L' if initial==8 else 'H'}\n({initial},0,0,\n0,0)", '#f5f5f5')
        arrow(ax, (.90, y), (1.08, y))
        box(ax, 1.10, y-.27, .85, .54, 'N\n(13,0,0,\n0,0)', '#eef5fa')
        ax.patches[-1].set_gid('fig1_witness_N')
        arrow(ax, (1.97, y), (2.20, y))
        ax.text(3.0, y, law, ha='center', va='center', fontsize=8, color=color)
    # The first connector occupies only the gap between the N boxes. The
    # second occupies a separate right-hand lane and links the law rows only.
    same, = ax.plot([1.95, 1.95], [1.475, 2.175], color='#444444', lw=.8)
    same.set_gid('fig1_same_A_connector')
    ax.text(2.06, 1.825, 'same current A', ha='left', va='center', fontsize=7)
    different, = ax.plot([3.83, 3.90, 3.90, 3.83], [2.45, 2.45, 1.20, 1.20], color='#444444', lw=.8)
    different.set_gid('fig1_different_B_connector')
    ax.text(4.10, 1.825, 'different B', rotation=90, ha='center', va='center', fontsize=7)
    fig.subplots_adjust(left=.018, right=.987, top=.925, bottom=.035, wspace=.085)
    return save(ctx, 'fig1', fig,
        r'\textbf{Two task layers and their history witness.} (a) A maps four records to five per-slot sums. '
        r'B uses their slot-1 category and the preceding mode to update the mode and determine the next-category law. '
        r'The annotations identify training conditions, not evidence that a network learned the depicted decomposition. '
        r'(b) The histories end on the same neutral sum board but retain different modes and require different laws. '
        r'Values are integer twelfths; law entries are ordered L/N/H. '
        rf'The task has {task["boards"]:,} completed sum boards and {task["histories"]:,} local histories. '
        r'Everything shown is exact task ground truth, not model output.', preview,
        task_checks={'legal_four_record_boards': checks, 'laws_order': 'L/N/H',
                     'previous_mode': 'off', 'training_strip_has_no_edges': True,
                     'category_arrow_source_slot': 1})


def fig2(ctx, preview):
    ctx.begin()
    for n in (8, 12, 13): ctx.registered(n)
    fig, axes = plt.subplots(2, 1, figsize=(6.5, 3.8), gridspec_kw={"height_ratios": [1, 1.35]})
    ax = axes[0]; ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
    ax.set_title("Recurrent architecture and the optional sums connection")
    box(ax, .01, .67, .13, .20, "records")
    box(ax, .22, .67, .20, .20, "shared raw carrier\nreset per round")
    box(ax, .50, .67, .24, .20, "upper recurrent state\nreset per episode")
    box(ax, .81, .67, .18, .20, "prediction\nnext-category law")
    arrow(ax, (.147, .77), (.213, .77)); arrow(ax, (.427, .77), (.493, .77))
    arrow(ax, (.747, .77), (.803, .77))
    from matplotlib.path import Path as PlotPath
    ax.add_patch(FancyArrowPatch(path=PlotPath([(.68,.875),(.68,.97),(.55,.97),(.55,.875)],
        [PlotPath.MOVETO,PlotPath.LINETO,PlotPath.LINETO,PlotPath.LINETO]),
        arrowstyle='-|>', mutation_scale=10, lw=.8, color='#444444'))
    box(ax, .23, .26, .18, .20, "sums output head")
    box(ax, .01, .26, .14, .20, "sums loss")
    arrow(ax, (.32, .663), (.32, .467)); arrow(ax, (.223, .36), (.157, .36))
    arrow(ax, (.418, .40), (.52, .663), linestyle="dashed")
    box(ax, .50, .06, .24, .21, "exact supplied sums\none-hot / numerical")
    arrow(ax, (.65, .277), (.65, .663))
    box(ax, .81, .34, .18, .17, "prediction loss")
    arrow(ax, (.90, .663), (.90, .517))
    box(ax, .80, .01, .19, .18, "probe / swap test")
    arrow(ax, (.745, .67), (.795, .15), linestyle="dotted")
    ax = axes[1]; ax.axis("off"); ax.set_title("Route and loss matrix")
    rows = [[LABELS['records'], "yes", "masked", "prediction loss"],
            [LABELS['supplied'], "yes", "exact frozen", "prediction loss"],
            [LABELS['sums'], "yes", "disconnected", "prediction + sums loss"],
            ["Connected (frozen)", "yes", "fixed sums output", "prediction + sums loss"],
            ["Connected (live)", "yes", "live sums output", "prediction + sums loss"],
            ["Numerical encoding", "yes", "exact numerical", "prediction loss"],
            ["Probability targets", "base version", "as the base version", "base losses; exact law"]]
    t = ax.table(cellText=rows, colLabels=["version / condition", "records route", "sums route", "loss"],
                 cellLoc="left", colWidths=[.40, .12, .24, .24], bbox=[0, 0, 1, 1])
    t.auto_set_font_size(False); t.set_fontsize(7)
    for (r, c), cell in t.get_celld().items():
        cell.set_linewidth(.4)
        if r == 0: cell.set_facecolor("#eeeeee")
    fig.subplots_adjust(left=.02, right=.98, bottom=.025, top=.93, hspace=.30)
    return save(ctx, "fig2", fig,
        r"Recoverability, computation and access are distinct measurements, not interchangeable routes. "
        r"(a) The sums output head and its loss attach to the shared carrier; a dashed optional connection "
        r"feeds sums output to prediction in the connected variants. (b) The matrix identifies the routes "
        r"and losses in the three versions and r13 variants; probability targets retain their base version's "
        r"routes and replace sampled targets with the exact law. The probe fits a reader on frozen states; the swap replaces an "
        r"aligned donor block, with selectivity checked separately. No measurement, seed average or control result "
        r"is implied by the icons; procedures and their calibration are in Appendix C.", preview)


def probe_panel(ax, ctx, study, family):
    if study == 8:
        records = ctx.ref("quantities", "r8_probes")
        rows = [(r["seed"], r["slot"], r["original"]["update0_accuracy"],
                 r["original"]["endpoint_accuracy"], r["original"]["majority_floor"])
                for r in records if r["probe_family"] == family]
        floors = ctx.ref("calibration", "8", "calibration", "probe", "oracle", "floors")
        oracle = ctx.ref("calibration", "8", "calibration", "probe", "oracle", "sites", "raw", family)
        shuffled = [r["shuffled_accuracy"] for r in floors]
        oracle_y = [r["accuracy"] for r in oracle]
    else:
        rows = [(r["seed"], r["slot"]+1, r["before"], r["endpoint"], r["majority_floor"])
                for r in ctx.ref("quantities", "r10_free_probes")]
        records = ctx.quantities["r10_free_probes"]
        # Saved per-seed controls on the same registered panel.
        shuffled = [records[j]["shuffled_accuracy"] for j in range(5)]
        oracle_y = [records[j]["positive_accuracy"] for j in range(5)]
        for r in records:
            ax.plot(r["slot"]+1+(r["seed"]-1)*.13, r["shuffled_accuracy"], "x", color="grey", ms=3)
            ax.plot(r["slot"]+1+(r["seed"]-1)*.13, r["positive_accuracy"], "+", color="black", ms=3)
    for seed, slot, before, end, floor in rows:
        x = slot + (seed-1)*.13
        ax.plot([x, x], [before, end], color=PALETTE["records"], lw=.7, alpha=.65)
        ax.plot(x, before, marker=MARKERS[seed], ms=4, mfc="white", mec=PALETTE["records"])
        ax.plot(x, end, marker=MARKERS[seed], ms=4, color=PALETTE["records"])
        ax.plot(x, floor, marker="_", ms=6, color="grey")
    ax.plot(range(1, 6), shuffled, color="grey", ls=":", label="shuffled labels")
    ax.plot(range(1, 6), oracle_y, color="black", ls="-.", label="measured oracle reader")
    ceiling(ax,1,'exact labels')
    ax.set(xticks=range(1, 6), xlabel="slot", ylabel="exact-sum probe accuracy", ylim=(-.04, 1.06),
           title=f"r{study} raw carrier, {family}" + (" (different task)" if study == 10 else ""))


def fig3(ctx, preview):
    ctx.begin(); natural_support(ctx); fig = plt.figure(figsize=(6.5, 4.6))
    grid = fig.add_gridspec(3, 2, left=.10, right=.98, top=.95, bottom=.24, hspace=.78, wspace=.42)
    # Same a–f order and receipts, with two wider rows of recovery/average
    # measures followed by the specific-failure panels rather than four tiny axes.
    left = [fig.add_subplot(grid[i, j]) for i,j in ((0,0),(0,1),(1,0),(1,1))]
    right = [fig.add_subplot(grid[2, 0]), fig.add_subplot(grid[2, 1])]
    probe_panel(left[0], ctx, 8, "linear"); probe_panel(left[1], ctx, 8, "mlp64")
    probe_panel(left[2], ctx, 10, "linear")
    for ax in left[:3]:
        ax.set_xlabel(''); ax.set_ylabel('probe accuracy' if ax is not left[1] else '')
        ax.set_title(ax.get_title().replace(' (different task)', ''))
    ax = left[3]
    for seed in range(3):
        v = ctx.ref("quantities", "r8_raw_KL", seed)
        ax.plot(seed-.07, v, marker=MARKERS[seed], color=PALETTE["records"], ms=5, label='r8' if seed==0 else None)
        v10=ctx.ref('control','10',f'free_original_seed{seed}','law_cases','natural','KL_bits')
        ax.plot(seed+.07,v10,marker=MARKERS[seed],mfc='white',mec=PALETTE['records'],ms=5,label='r10' if seed==0 else None)
    floor = ctx.ref("calibration", "8", "calibration", "B", "original", "current_board_null", "natural_excess_KL_bits")
    ax.axhline(floor, color="#8c564b", ls=(0,(5,2)), label="r8 board-only floor")
    blind=ctx.ref('calibration','10','calibration','mode_blind','original','natural','KL_bits')
    ax.axhline(blind,color='grey',ls='-.',label='r10 mode-blind floor')
    ax.set(xticks=range(3), xlabel="", ylabel="natural KL (bits)", title="r8 / r10 natural KL")
    ax.set_yscale("log")
    ax = right[0]
    for seed, v in enumerate(ctx.ref("quantities", "r8_law_TV")):
        ax.plot(seed-.07, v, marker=MARKERS[seed], color=PALETTE["records"], ms=5,label='r8' if seed==0 else None)
        v10=ctx.ref('control','10',f'free_original_seed{seed}','law_cases','law_rows','maximum_TV')
        ax.plot(seed+.07,v10,marker=MARKERS[seed],mfc='white',mec=PALETTE['records'],ms=5,label='r10' if seed==0 else None)
    floor = ctx.ref("calibration", "8", "calibration", "B", "original", "current_board_null", "mode_law", "maximum_TV")
    ax.axhline(floor, color="#8c564b", ls=(0,(5,2)), label="r8 board-only floor")
    ax.axhline(ctx.ref('calibration','10','calibration','mode_blind','original','law_rows','maximum_TV'),color='grey',ls='-.',label='r10 mode-blind floor')
    ax.axhline(.02, color="#D55E00", ls="-.", label="r8 bar 0.02"); ceiling(ax)
    ax.axhline(.05, color=PALETTE['frozen'], ls=(0,(3,1,1,1)), label='r10 original bar 0.05')
    ax.set(xticks=range(3), xlabel="seed", ylabel="law TV\n(maximum)", title="r8 / r10 law TV")
    ax = right[1]
    for seed in range(3):
        d = ctx.ref("control", "12", f"uniform_original_seed{seed}", "census_all_four_renderings_and_r9",
                    "registered_rendering", "by_slot1_sum_twelfths")
        xs = sorted(map(int, d))
        ax.plot(xs, [d[str(x)]["categorical_misreads"] for x in xs], color=PALETTE["records"],
                marker=MARKERS[seed], ms=2.5)
    d = ctx.ref("calibration", "12", "calibration", "untrained_census", "original", "registered_rendering", "by_slot1_sum_twelfths")
    xs = sorted(map(int, d))
    ax.plot(xs, [d[str(x)]["categorical_misreads"] for x in xs], color="grey", ls=(0,(1,1,4,1)), label="untrained census")
    ceiling(ax); ax.axvspan(11, 13, color="#aaaaaa", alpha=.15); ax.axvspan(23, 25, color="#aaaaaa", alpha=.15)
    ax.set(xlabel="slot-1 sum (twelfths)", ylabel="misreads\n(boards)", title="r12 census, rendering 0")
    ax.set_yscale("symlog", linthresh=1)
    for x, label in ((12, '11–13'), (24, '23–25')):
        ax.text(x, 1.02, label, transform=ax.get_xaxis_transform(), ha='center', fontsize=7)
    # Reserve the band labels' own strip, below the panel title.
    ax._paper_title_pad = 10
    for axis in [*left[:3], *right]:axis.set_ylim(bottom=0)
    from matplotlib.lines import Line2D
    keys=[Line2D([],[],marker=m,color='black',ls='',label=f'seed {s}') for s,m in enumerate(MARKERS)]
    fig.legend(handles=keys,loc='lower center',bbox_to_anchor=(.5,.005),ncol=3,frameon=False)
    # Keys have separate, explicit scopes; no r8/r10 key describes probes.
    controls={}
    for axis in [*left,*right]:
        hs,ls=axis.get_legend_handles_labels()
        for h,l in zip(hs,ls):
            if l not in ('r8','r10'): controls.setdefault(l,h)
    fig.legend(controls.values(),controls,loc='lower center',bbox_to_anchor=(.5,.035),ncol=3,frameon=False)
    return save(ctx, "fig3", fig,
        r"Recoverable sums and low average error coexist with specific failures. "
        r"(a,b) r8 linear/MLP; (c) r10 linear: slots 1–5, 512 held-out boards/slot, majority ticks, shuffled floors "
        r"and oracle ceiling. Open/filled: update 0/20k (a–c), r10/r8 (d,e); shapes: seeds 0/1/2. "
        r"(d) Natural KL: 60,000 positions, board-only/mode-blind floors; the log axis omits the oracle's 0 bits. "
        r"(e) Law TV: 576 r8 histories/180 r10 rows, zero oracle, r8 bar 0.02 and r10 original-law "
        r"0.05 bar (its equal-law bar is 0.02). (f) r12 uniform categorical misreads: 24,435 boards, rendering 0, "
        r"untrained floor, shaded cutoff bands. Compare seeds within panels; r8/r10 comparisons are "
        r"historical and tasks differ. Paired probe intervals: Appendix E.", preview)


def mechanism(ax, ctx, values, labels, title, ylabel, floor_rows=None, tv=False):
    for j, (condition, yy) in enumerate(values):
        color = condition_color(condition)
        for s, y in enumerate(yy):
            x = j+(s-1)*.13
            ax.plot(x, y, marker=MARKERS[s], ms=5, color=color)
            if floor_rows is not None:
                ax.plot(x, floor_rows[j][s], marker="x", ms=3, color="grey")
    ceiling(ax)
    if tv: ax.axhline(.02, ls="-.", color="#D55E00", lw=.8, label="bar 0.02")
    ax.set(xticks=range(len(values)), xticklabels=labels, title=title, ylabel=ylabel)
    if not tv: ax.set_yscale("symlog", linthresh=1 if "misread" in ylabel or not ylabel else 1e-5)
    ax.set_ylim(bottom=0)
    ax.set_ylim(top=max(ax.dataLim.ymax, .02)*(1.8 if ax.get_yscale() != 'linear' else 1.18))
    # Direct condition labels are the colour key, outside the data rectangle.
    for label, (condition, _) in zip(ax.get_xticklabels(), values):
        label.set_color(condition_color(condition))


def run13(ctx, experiment, condition, seed):
    return next(k for k, r in ctx.sources["control"]["13"].items()
                if r["run"] == {"experiment": experiment, "condition": condition, "law": "original", "seed": seed})


def fig4(ctx, preview):
    ctx.begin(); natural_support(ctx); fig, axs = plt.subplots(3, 2, figsize=(6.5, 4.6))
    noise = ctx.ref("quantities", "r13_noise")
    for i, kind in enumerate(("raw", "sums")):
        conditions = [kind+"_sampled", kind+"_probability"]
        floor = [[ctx.ref("control", "13", run13(ctx, "noise", c, s), "learning_curve", 0,
                          "categorical_misreads") for s in range(3)] for c in conditions]
        mechanism(axs[0, i], ctx, [(c, noise[c]) for c in conditions],
                  ["sampled", "probability"], "noise: " + ("prediction loss" if kind == "raw" else "prediction + sums loss"),
                  "misreads (boards)" if i==0 else "", floor)
    access = ctx.ref("quantities", "r13_access")
    conditions = ["disconnected", "frozen", "live", "exact"]
    colors = ["sums", "frozen", "live", "supplied"]
    for ax, field, ylabel in [(axs[1, 0], "categorical_misreads", "misreads (boards)"),
                              (axs[1, 1], "KL_bits", "natural KL (bits)"),
                              (axs[2, 0], "long_TV", "long-panel law TV")]:
        curve_field = {"categorical_misreads": "categorical_misreads", "KL_bits": "natural_KL_bits", "long_TV": "law_maximum_TV"}[field]
        floor = [[ctx.ref("control", "13", run13(ctx, "access", c, s), "learning_curve", 0, curve_field)
                  for s in range(3)] for c in conditions]
        # The archived update-0 curve stores the full-law maximum, not the
        # long-panel maximum: do not mislabel it as a matched long-only floor.
        if field == "long_TV":
            floor = None
            for j, c in enumerate(conditions):
                for s in range(3):
                    r = ctx.sources["control"]["13"][run13(ctx, "access", c, s)]
                    rec = r["audit_references"][0]
                    initial, eid = ctx.referenced(rec)
                    floor_value = initial["audit"]["mode_law"]["rows"]
                    if floor_value is None:
                        raise ValueError("initial long-panel floor not available at expected audit interface")
                    vals = [v["maximum_TV"] for key, v in floor_value.items() if key[-1:].isdigit() and int(key[-1]) >= 3]
                    ctx.ref(eid, "audit", "mode_law", "rows")
                    axs[2, 0].plot(j+(s-1)*.13, max(vals), marker="x", color="grey", ms=3)
        mechanism(ax, ctx, [(co, [r[field] for r in access[c]]) for co, c in zip(colors, conditions)],
                  ["(1)", "(2)", "(3)", "(4)"], "access (matched)", ylabel, floor, tv=field == "long_TV")
    enc = ctx.ref("quantities", "r13_encoding")
    floor = [[ctx.ref("control", "13", run13(ctx, "access" if c == "onehot" else "encoding",
                       "exact" if c == "onehot" else c, s), "learning_curve", 0, "categorical_misreads")
              for s in range(3)] for c in ("onehot", "numerical")]
    mechanism(axs[2, 1], ctx, [("supplied", enc["onehot"]), ("numerical", enc["numerical"])],
              ["one-hot", "numerical"], "encoding (matched)", "misreads (boards)", floor)
    # A true log axis shows the positive KL values and controls only; its
    # exact oracle at zero is explicitly qualified in the caption.
    kl_ax = axs[1, 1]
    positive = [y for line in kl_ax.lines for y in line.get_ydata() if y > 0]
    kl_ax.set_yscale('log')
    kl_ax.set_ylim(min(positive)/1.8, max(positive)*1.8)
    axs[0, 0].plot([], [], 'x', color='grey', label='matched update 0')
    for i,condition in enumerate(conditions,1):
        axs[1,0].plot([],[],color=condition_color(condition),label=f'({i}) '+condition_label(condition))
    shared_legend(fig, axs, y=.005, ncol=2)
    panel_letters(fig); fig.tight_layout(pad=1.0, h_pad=.8, w_pad=1.2, rect=(0, .17, 1, .99))
    return save(ctx, "fig4", fig,
        r"Target noise, access and encoding affect measured errors without guaranteeing prediction closure. "
        r"Matched r13 comparisons: targets within versions (a,b), numbered access variants (c–e), "
        r"encodings of exact sums (f). Shapes: seeds 0/1/2; grey crosses: matched update 0; dashed line: "
        r"zero-error oracle except in (d), whose 0-bit oracle lies outside the logarithmic axis. "
        r"Categorical misreads: 24,435 boards, rendering 0; natural KL: 60,000 "
        r"positions; maximum long-panel TV: 384 N3–N8 endpoints, bar 0.02. No pooled means or bands. "
        r"Controls are matched within panels.", preview)


def erosion_readouts(ctx, seed, condition):
    """Bind the exact start separately from the first post-update readout."""
    key = f"erosion_{condition}_original_seed{seed}"
    initial = ctx.ref('control', '11', key, 'B_A_curve', 0)
    if initial['step'] != 0 or initial['A_vector_accuracy'] != 1.0:
        raise ValueError('r11 update-0 board audit is not exact; refuse exact-start figure')
    rows = ctx.ref('control', '11', key, 'early_erosion_readouts')
    if [r['step'] for r in rows] != [1, 5, 10, 50, 100]:
        raise ValueError('r11 early readout update indices differ')
    return [0]+[r['step'] for r in rows], [initial['A_vector_accuracy']]+[
        r['A_board_accuracy']['vector']['correct']/r['A_board_accuracy']['vector']['total'] for r in rows]


def erosion_series(ctx, seed, condition):
    """One evidence-bound series for the update and movement views."""
    key = run13(ctx, "erosion", condition, seed)
    ref = ctx.ref("control", "13", key, "records")
    rows, eid = ctx.referenced(ref)
    series = ctx.ref("control", "13", key, "accuracy_curve")
    if series != [[r["step"], r["local"]["correct"]] for r in rows]:
        raise ValueError("movement/exactness differs from ledger accuracy curve")
    if any(r['local']['total'] != 1555 for r in rows):
        raise ValueError('local-history denominator differs')
    return rows, series, eid


def fig5(ctx, preview):
    ctx.begin(); fig, axs = plt.subplots(2, 3, figsize=(6.5, 3.8))
    update1={c:[] for c in ('adam','reduced','sgd','blocked')}
    for seed in range(3):
        ax = axs[0, seed]
        for condition, color in (("b_only", "records"), ("a_plus_b", "sums")):
            steps, scores = erosion_readouts(ctx, seed, condition)
            ax.plot(steps, scores, marker=MARKERS[seed], ms=3, color=PALETTE[color],
                    label="prediction loss" if condition == "b_only" else "prediction + sums loss")
        ceiling(ax, 1, "exact update 0 / oracle")
        ax.set(title=f"r11, seed {seed}", xlabel="update", ylabel="board-vector\nexactness" if seed==0 else "", ylim=(-.03, 1.07))
        ax.set_xscale('symlog', linthresh=1)
        ax.set_xlim(-.1, 110)
        ax.set_xticks([0, 1, 5, 100], labels=['0', '1', '5', '100'])
        for condition in ("adam", "reduced", "sgd", "blocked"):
            rows, series, _ = erosion_series(ctx, seed, condition)
            first=require_series([r for r in rows if r['step']==1], f'{condition} update 1')[0]
            if first['local']['total']!=1555: raise ValueError('local-history denominator differs')
            update1[condition].append(first['local']['correct'])
            ax = axs[1, seed]
            ax.plot([r[0] for r in series], [r[1]/1555 for r in series], color=PALETTE[condition], label=LABELS[condition])
            ctx.ref("quantities", "r13_erosion")
        ax = axs[1, seed]; ceiling(ax, 1, "exact update 0 / oracle")
        ax.set(ylim=(-.03, 1.07), ylabel="local exactness" if seed==0 else "", xlabel="update")
        axs[1, seed].set_title(f"r13, seed {seed}")
        axs[1, seed].set_xscale('symlog', linthresh=1)
        axs[1, seed].set_xlim(-.1, 210)
        axs[1, seed].set_xticks([0, 1, 10, 100], labels=['0', '1', '10', '100'])
    shared_legend(fig, axs[0], y=.93, ncol=3)
    shared_legend(fig, axs[1:], y=.005, ncol=3)
    panel_letters(fig); fig.tight_layout(pad=.7, h_pad=.9, w_pad=.8, rect=(0, .15, 1, .95))
    counts='; '.join(LABELS[c]+': '+ ' / '.join(f'{v:,}' for v in update1[c]) for c in update1)
    return save(ctx, "fig5", fig,
        r"Prediction gradients erode exact sums at update 1, not uniquely under AdamW. "
        r"Columns: seeds 0–2. (a–c) Compare r11 losses: exact starts on 24,435 boards; "
        r"updates 1/5/10/50/100 use a fixed 128-board subset. Symlog separates 0/1. "
        r"(d–f) r13, all 1,555 local histories: "
        r"every tested active optimizer loses exactness at update 1. "
        +"Update-1 correct counts, seeds 0/1/2, each out of 1,555: "+counts+". "+
        r"Blocked prediction gradient is a separate weight-decay control; dashed line: exact start/oracle. "
        r"Movement-matched points: \cref{fig:appendix_D_movement}. r11/r13 is historical; no pooling or bands.", preview)


def erosion_movement(ctx, preview):
    ctx.begin(); fig, axs = plt.subplots(1, 3, figsize=(6.5, 2.2))
    aggregate = ctx.evidence.entries["repo/"+ledger_supplement(ctx)]
    ranges = ctx.manifest_json(aggregate)["erosion_comparisons"]
    for seed, ax in enumerate(axs):
        bound = ranges[seed]["observed_ranges"]["adam--sgd--reduced"]["range"][1]
        ctx.ref(aggregate["id"], "erosion_comparisons", seed, "observed_ranges",
                "adam--sgd--reduced", "range")
        for condition in ("adam", "reduced", "sgd"):
            rows, series, eid = erosion_series(ctx, seed, condition)
            movement = [ctx.ref(eid, j, "cumulative_path") for j in range(len(rows))]
            keep = [j for j, x in enumerate(movement) if x <= bound]
            require_series(keep, f'common movement {condition} seed {seed}')
            ax.plot([movement[j] for j in keep], [series[j][1]/1555 for j in keep],
                    color=PALETTE[condition], marker=".", ms=2, label=LABELS[condition])
        ceiling(ax, 1, "exact start / oracle")
        ax.set(title=f"r13, seed {seed}", xlabel="cumulative movement",
               ylabel="local exactness" if seed==0 else "", ylim=(-.03, 1.07))
    shared_legend(fig, axs, y=.005, ncol=4)
    panel_letters(fig); fig.tight_layout(pad=.7, w_pad=.8, rect=(0, .16, 1, .98))
    return save(ctx, "appendix_D_movement", fig,
        r"Exact sums erode across active optimizers at common recorded movement. "
        r"(a–c) Seeds 0–2, all 1,555 local histories. Compare AdamW, reduced-rate AdamW and SGD "
        r"within each seed's three-active-arm common range; points are observed, not interpolated. "
        r"Blocked prediction gradient is excluded from that range and remains a separate control "
        r"in \cref{fig:fig5}. Dashed line: exact start/oracle. No pooled means or confidence bands.", preview)


def ledger_supplement(ctx):
    return "reports/phase11/oldgame_memory/multiround/study_r13_mechanism/aggregate.json"


def methods(ctx, preview):
    ctx.begin(); ctx.ref("calibration", "10", "calibration", "interpretation_scope")
    fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.7))
    for ax in axs: ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
    axs[0].set_title('Frozen-state probe'); axs[1].set_title('Selective swap test')
    box(axs[0], .04, .57, .34, .25, "frozen states\ntraining identities")
    box(axs[0], .55, .57, .40, .25, "fit reader\ntrain-only statistics")
    arrow(axs[0], (.38, .69), (.55, .69))
    box(axs[0], .20, .05, .65, .30, "held-out identities\nmajority / shuffled / oracle controls")
    arrow(axs[0], (.74, .57), (.64, .35))
    box(axs[1], .04, .62, .42, .25, "donor state\naligned slot block")
    box(axs[1], .55, .62, .42, .25, "recipient state\nreplace one block")
    arrow(axs[1], (.46, .74), (.55, .74))
    box(axs[1], .13, .02, .78, .37, "donor-follow AND other-slot selectivity\npositive / no-op / shuffled alignment\ncalibration is not measured use")
    arrow(axs[1], (.77, .62), (.67, .39))
    fig.subplots_adjust(left=.01, right=.99, top=.87, bottom=.02, wspace=.12)
    return save(ctx, "appendix_C_methods", fig,
                "Separate probe (a) and swap-test (b) procedures. Readers and alignment fit on training identities "
                "only; scoring identities are held out. Positive, no-op and shuffled controls calibrate the "
                "procedure, while donor-follow and selectivity concern the evaluated carrier. This schematic "
                "has no empirical seed average or accuracy; full controls and support are in Appendix C.", preview)


def learning(ctx, preview, study, group=None):
    ctx.begin(); natural_support(ctx)
    rows = ctx.sources["control"][str(study)]
    selected=[(name,row) for name,row in rows.items() if
        (study!=11 or name.startswith(group+'_')) and (study!=13 or row['run']['experiment']==group)]
    equal=any('_equal_' in name or row.get('run',{}).get('law')=='equal' for name,row in selected)
    nrows=2 if equal else 1
    fig, axs = plt.subplots(nrows, 3, figsize=(6.5, 5.8 if equal else 3.3), squeeze=False)
    for name, row in rows.items():
        if study == 11 and not name.startswith(group+"_"): continue
        if study == 13 and row["run"]["experiment"] != group: continue
        if study == 13: seed, law, condition = row["run"]["seed"], row["run"]["law"], row["run"]["condition"]
        else:
            seed = int(name[-1]); law = "equal" if "_equal_" in name else "original"
            condition = name.split("_"+law+"_")[0].replace((group or "")+"_", "", 1) if group else name.split("_"+law+"_")[0]
        field = next((k for k in ("loss_KL_curve", "B_curve", "B_A_curve", "learning_curve") if k in row), None)
        if field is None: continue
        curve = ctx.ref("control", str(study), name, field)
        ys = [r.get("natural_excess_KL_bits", r.get("natural_KL_bits", r.get("natural_KL"))) for r in curve]
        require_series(curve, name)
        if any(y is None for y in ys): raise ValueError(f'missing learning value: {name}')
        ax = axs[int(law == "equal"), seed]
        color = condition_color(condition)
        ax.plot([r["step"] for r in curve], ys, color=color, label=condition_label(condition))
        ax.plot(curve[0]["step"], ys[0], marker="o", mfc="white", mec=color, ms=4)
    for i in range(nrows):
        for s in range(3):
            ax = axs[i, s]; ceiling(ax)
            if len(ax.lines) == 1: ax.text(.5,.5,'not run',transform=ax.transAxes,ha='center',fontsize=8)
            ax.set_title(f"{'original' if i == 0 else 'equal control'}, seed {s}")
            ax.set(xlabel="update", ylabel="natural KL (bits)"); ax.set_yscale("symlog", linthresh=1e-6)
            ax.margins(x=.06,y=.10)
            ax.set_ylim(bottom=-1e-7,top=max(ax.dataLim.ymax,1e-6)*1.2)
            ax.ticklabel_format(axis="x", style="sci", scilimits=(3, 3))
    shared_legend(fig, axs, y=.005, ncol=2)
    panel_letters(fig); fig.tight_layout(pad=1.1, rect=(0, .18 if equal else .25, 1, .96))
    return save(ctx, f"appendix_D_r{study}" + ("_"+group if group else ""), fig,
        f"Recorded r{study} " + (group+" " if group else "") +
        "learning curves show changes in average error, not sufficient evidence of reliable competence. "
        "Every seed and condition is retained; (a–c) original"+ (" and (d–f) equal laws are separate rows" if equal else "; no equal-law arms were run") +
        ", in seed order 0–2. "
        "Open points mark each condition's own update-0 control; dashed zero is the exact oracle. "
        "The quantity is natural KL in bits on 5,000 natural episodes of 12 rounds (60,000 scored positions), not a loss "
        "or a census frequency. No smoothing, selected checkpoint or across-seed band is used. "
        "Compare conditions within the same seed and law only; cross-study comparisons are historical. "
        "Natural KL alone does not establish reliability.", preview)


def condition_color(c):
    return PALETTE.get(c, {"raw_only": PALETTE["records"], "free": PALETTE["records"], "uniform": PALETTE["records"],
        "a_only": PALETTE["supplied"], "dual": PALETTE["frozen"], "a_supplied": PALETTE["supplied"],
        "a_target": PALETTE["sums"], "a_forced": PALETTE["supplied"], "free_a": PALETTE["sums"],
        "raw_sampled": PALETTE["records"], "raw_probability": PALETTE["live"], "sums_sampled": PALETTE["sums"],
        "sums_probability": PALETTE["frozen"], "disconnected": PALETTE["sums"], "exact": PALETTE["supplied"],
        "onehot": PALETTE["supplied"], "b_only": PALETTE["records"], "a_plus_b": PALETTE["sums"],
        "cutoff": PALETTE["live"], "decoy": PALETTE["frozen"], "dose1": PALETTE["records"],
        "dose10": PALETTE["live"], "dose100": PALETTE["sums"]}.get(c, "#595959"))


def condition_label(c):
    return condition_name(c).replace('→',r'$\to$')


def geometry(ctx, preview):
    ctx.begin(); a = ctx.evidence.load(ledger_supplement(ctx)); rows = a["supplementary"]["rows"]
    entry = ctx.evidence.entries["repo/"+ledger_supplement(ctx)]
    ctx.manifest_json(entry)
    fig, axs = plt.subplots(2, 3, figsize=(6.5, 5.8))
    for seed in range(3):
        for condition in ("raw_sampled", "raw_probability"):
            selected = [r for r in rows if r["run"]["seed"] == seed and r["run"]["condition"] == condition]
            selected.sort(key=lambda r: r["step"])
            require_series(selected, f'geometry {condition} seed {seed}')
            for j, pair in enumerate(([12, 13], [23, 24])):
                measured = [next(m for m in r["measured"] if m["sums"] == pair) for r in selected]
                xs = [r["step"] for r in selected]
                for r in selected: ctx.ref(entry["id"], "supplementary", "rows", rows.index(r), "measured")
                for row, field in ((0, "accuracy"), (1, "cross_entropy_nats")):
                    ax = axs[row, seed]
                    ax.plot(xs, [m["reader"][field] for m in measured], color=condition_color(condition),
                            marker="o" if j == 0 else "s", ms=3, ls="-" if j == 0 else "--",
                            label=condition_label(condition) if j == 0 else None)
                    ax.plot(xs, [m["label_permutation_floor"][field] for m in measured], color="grey", ls=":" , marker="x", ms=2,label='shuffled labels' if j==0 else None)
        ceiling(axs[0, seed], 1); ceiling(axs[1, seed], 0)
        axs[0, seed].axhline(.5, color="grey", ls=":", label="balanced constant carrier")
        axs[1, seed].axhline(np.log(2), color="grey", ls=":")
        for row, ylabel in ((0, "held-out discrimination accuracy"), (1, "held-out cross-entropy (nats)")):
            axs[row, seed].set(title=f"seed {seed}", xlabel="saved update", ylabel=ylabel)
    from matplotlib.lines import Line2D
    axs[0,0].add_line(Line2D([],[],color='black',marker='o',ls='-',label='12/13 pair'))
    axs[0,0].add_line(Line2D([],[],color='black',marker='s',ls='--',label='23/24 pair'))
    shared_legend(fig, axs, y=.005, ncol=3)
    panel_letters(fig); fig.tight_layout(pad=1.1, rect=(0, .16, 1, .96))
    return save(ctx, "appendix_E_geometry", fig,
        r"Cutoff discrimination can succeed while prediction still fails. The supplementary panel was bound "
        r"before states were read, with disjoint fit/evaluation identities and fixed renderings. Three seed "
        r"columns show saved 0/5k/20k sampled- and probability-target prediction-loss checkpoints only, with no network updates: "
        r"(a–c) accuracy and (d–f) cross-entropy, in seed order 0–2. Compare "
        r"sampled- and probability-target readers for the same seed and pair; circles/solid lines are 12/13 "
        r"(135 fitting pairs, 150 evaluation pairs; 300 endpoint labels), squares/dashed lines are 23/24 (12/13 pairs; "
        r"26 labels). Grey crosses are the saved shuffled-label floors; balanced constant floors are 0.5 "
        r"accuracy and ln 2 loss, and the exact ceiling is 1 accuracy / 0 loss. No confidence bands are "
        r"implied. Distances and rendering variation remain descriptive in Appendix E's support tables; "
        r"successful discrimination is not proof of predictive use or of a precision ceiling.", preview)


FIGURES = {"fig1": fig1, "fig2": fig2, "fig3": fig3, "fig4": fig4, "fig5": fig5,
           "appendix_D_movement": erosion_movement,
           "appendix_C_methods": methods, "appendix_E_geometry": geometry}
for _study, _groups in ((8, [None]), (10, [None]), (11, ["rarity", "dose", "erosion"]), (12, [None]),
                        (13, ["noise", "access", "encoding"])):
    for _group in _groups:
        _name = f"appendix_D_r{_study}" + ("_"+_group if _group else "")
        FIGURES[_name] = lambda ctx, preview, n=_study, g=_group: learning(ctx, preview, n, g)
