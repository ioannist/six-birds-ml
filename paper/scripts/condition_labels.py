"""One explicit glossary-bound version/variant registry for all paper assets."""
from pathlib import Path
import re

NAMES = {
    'raw_only': 'records → prediction', 'free': 'records → prediction',
    'free_a': 'records → prediction+sums', 'a_target': 'records → prediction+sums',
    'a_only': 'records+sums → prediction (sums route only)',
    'a_forced': 'records+sums → prediction (sums route only)',
    'dual': 'records+sums → prediction', 'a_supplied': 'records+sums → prediction',
    'uniform': 'records → prediction (uniform sampling)',
    'cutoff': 'records → prediction (cutoff coverage)',
    'decoy': 'records → prediction (decoy coverage)',
    'disconnected': 'records → prediction+sums',
    'frozen': 'Connected (frozen)', 'live': 'Connected (live)',
    'exact': 'records+sums → prediction (exact supplied)',
    'onehot': 'records+sums → prediction (one-hot encoding)',
    'numerical': 'records+sums → prediction (Numerical encoding)',
    'raw_sampled': 'records → prediction (sampled targets)',
    'raw_probability': 'records → prediction (Probability targets)',
    'sums_sampled': 'records → prediction+sums (sampled targets)',
    'sums_probability': 'records → prediction+sums (Probability targets)',
    'erosion_b_only': 'records → prediction (Erosion continuation)',
    'erosion_a_plus_b': 'records → prediction+sums (Erosion continuation)',
    'adam': 'AdamW', 'reduced': 'reduced-lr AdamW', 'sgd': 'SGD',
    'blocked': 'blocked prediction gradient',
    **{f'dose_dose{n}': f'records → prediction+sums (sums dose {n}%)' for n in (1,10,100)},
}


def allowed_labels(root=None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    text = (root/'paper/notes/notation_and_terminology.md').read_text()
    section = text.split('## Asset version/variant labels\n',1)[1].split('\n## ',1)[0]
    return set(re.findall(r'^- \*\*(.*?)\*\*',section,re.M))


def validate_label(label, root=None):
    text = re.sub(r'^r\d+[: ]+','',label)
    text = re.sub(r'\s*/\s*(?:seed\s*)?\d+(?:\s+(?:original|equal))?$','',text)
    if text not in allowed_labels(root):
        raise ValueError(f'condition label is not in the glossary: {label}')
    return label


def condition_name(condition):
    if condition.startswith('rarity_'):
        condition = condition.removeprefix('rarity_')
    condition = {'b_only':'erosion_b_only','a_plus_b':'erosion_a_plus_b',
                 'dose1':'dose_dose1','dose10':'dose_dose10','dose100':'dose_dose100'}.get(condition,condition)
    if condition not in NAMES:
        raise ValueError(f'unknown condition: {condition}')
    return validate_label(NAMES[condition])
