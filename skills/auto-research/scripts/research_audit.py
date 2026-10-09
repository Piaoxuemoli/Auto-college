"""Offline research ledger initializer and consistency audit; Python 3.9+ stdlib.

No model/API calls, scheduling, training, publishing or automatic resumption.
The audit checks recorded evidence, not scientific truth. JSON is written to stdout.
"""
import argparse
import datetime
import json
import math
import pathlib
import re
import statistics
import sys

CHECKS = ('scientific_review', 'citation_review', 'numeric_review', 'compilation', 'visual_review')
KINDS = {'empirical', 'theoretical', 'literature', 'proposal'}
STATUSES = {'supported', 'refuted', 'inconclusive', 'untested'}


def project_path(root, value):
    if not isinstance(value, str) or not value:
        raise ValueError('Evidence path must be a nonempty relative string')
    if pathlib.PureWindowsPath(value).is_absolute() or pathlib.Path(value).is_absolute():
        raise ValueError('Evidence path must be project-relative: ' + value)
    target = (root / value).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        raise ValueError('Evidence path escapes the project: ' + value)
    return target


def load_records(path):
    if not path.is_file():
        raise ValueError('Missing ledger: ' + path.name)
    rows = []
    for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError('%s line %s must be an object' % (path.name, number))
        rows.append(value)
    return rows


def dotted(row, key):
    value = row
    for part in key.split('.'):
        value = value[part]
    return value


def finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('Expected finite numeric value, got ' + repr(value))
    return value


def source_number(root, spec):
    path = project_path(root, spec['source_file'])
    if path.suffix.lower() == '.jsonl':
        rows = load_records(path)
    else:
        value = json.loads(path.read_text(encoding='utf-8-sig'))
        rows = value if isinstance(value, list) else [value]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError('Numeric source must contain objects')
    where = spec.get('where', {})
    if not isinstance(where, dict):
        raise ValueError('where must be an object')
    selected = [r for r in rows if all(dotted(r, k) == v for k, v in where.items())]
    if not selected:
        raise ValueError('Numeric selector returned zero records')
    unit_key = spec.get('unit_id_key')
    if unit_key:
        ids = [json.dumps(dotted(r, unit_key), sort_keys=True) for r in selected]
        if len(ids) != len(set(ids)):
            raise ValueError('Repeated unit IDs; aggregate to the intended unit first')
    operation = spec.get('operation', 'identity')
    if operation == 'count':
        actual = len(selected)
    else:
        values = [finite_number(dotted(r, spec['key'])) for r in selected]
        if operation == 'identity':
            if len(values) != 1:
                raise ValueError('identity requires exactly one selected record')
            actual = values[0]
        elif operation == 'mean':
            actual = statistics.mean(values)
        elif operation == 'std':
            if len(values) < 2:
                raise ValueError('Sample std requires at least two records')
            actual = statistics.stdev(values)
        elif operation == 'sum':
            actual = sum(values)
        else:
            raise ValueError('Unknown operation: ' + str(operation))
    return finite_number(actual * finite_number(spec.get('scale', 1)))


def initialize(root, topic):
    names = ['RUN_STATE.json', 'PROJECT_CONTEXT.md', 'ROADMAP.md', 'ledger/claims.jsonl', 'ledger/references.jsonl']
    if any((root / name).exists() for name in names):
        raise ValueError('Research state already exists; resume it instead of reinitializing')
    root.mkdir(parents=True, exist_ok=True)
    for folder in ['ledger', 'paper', 'experiments', 'results', 'figures', 'reviews']:
        (root / folder).mkdir(exist_ok=True)
    state = {
        'schema_version': '1.0', 'topic': topic, 'phase': 'S0',
        'deliverable_level': 'plan', 'manuscript': None,
        'checks': {key: 'pending' for key in CHECKS}, 'check_evidence': {},
        'not_applicable_reasons': {}, 'next_action': 'Read the supplied materials and define the testable question',
        'autostart': False, 'authorization': 'Execution requires the current user request; no permissions imported',
        'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    (root / 'RUN_STATE.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    assets = pathlib.Path(__file__).resolve().parent.parent / 'assets'
    for name in ['PROJECT_CONTEXT', 'ROADMAP']:
        text = (assets / (name + '.template.md')).read_text(encoding='utf-8')
        (root / (name + '.md')).write_text(text + '\n主题：' + topic + '\n', encoding='utf-8')
    for name in ['claims', 'references']:
        (root / 'ledger' / (name + '.jsonl')).write_text('', encoding='utf-8')
    return {'initialized': True, 'root': str(root), 'phase': 'S0', 'autostart': False}


def audit(root):
    issues = []
    warnings = []
    numeric_checks = []
    state = json.loads((root / 'RUN_STATE.json').read_text(encoding='utf-8-sig'))
    refs = load_records(root / 'ledger/references.jsonl')
    claims = load_records(root / 'ledger/claims.jsonl')
    level = state.get('deliverable_level')
    if level not in {'plan', 'draft', 'complete', 'submission_candidate'}:
        issues.append('Invalid deliverable_level')
    if state.get('autostart') is not False:
        issues.append('autostart must be false')
    by_ref = {}
    for ref in refs:
        key = ref.get('id')
        if not isinstance(key, str) or not key or key in by_ref:
            issues.append('Missing or duplicate reference ID: ' + repr(key))
            continue
        by_ref[key] = ref
        if ref.get('status') not in {'verified', 'partial', 'unresolved', 'excluded'}:
            issues.append('Invalid reference status: ' + key)
        if ref.get('status') == 'verified':
            try:
                for field in ['title', 'authors', 'year', 'venue', 'url', 'checked_at', 'verification_file']:
                    if not ref.get(field):
                        raise ValueError('Missing ' + field)
                if not project_path(root, ref['verification_file']).is_file():
                    raise ValueError('Verification note does not exist')
            except (ValueError, TypeError) as exc:
                issues.append('Reference ' + key + ': ' + str(exc))
    claim_ids = set()
    primaries = []
    for claim in claims:
        key = claim.get('id')
        if not isinstance(key, str) or not key or key in claim_ids:
            issues.append('Missing or duplicate claim ID: ' + repr(key))
            continue
        claim_ids.add(key)
        if not claim.get('text') or claim.get('kind') not in KINDS or claim.get('status') not in STATUSES:
            issues.append('Invalid claim content/kind/status: ' + key)
        if claim.get('role') not in {'primary', 'mechanism', 'boundary', 'background'}:
            issues.append('Invalid claim role: ' + key)
        if claim.get('role') == 'primary':
            primaries.append(claim)
        evidence = claim.get('evidence_files', [])
        if not isinstance(evidence, list):
            issues.append('evidence_files must be a list: ' + key)
            evidence = []
        for filename in evidence:
            try:
                if not project_path(root, filename).is_file():
                    issues.append('Missing evidence for ' + key + ': ' + filename)
            except ValueError as exc:
                issues.append(str(exc))
        cited = claim.get('reference_ids', [])
        if not isinstance(cited, list):
            issues.append('reference_ids must be a list: ' + key)
            cited = []
        for ref_id in cited:
            if ref_id not in by_ref or by_ref[ref_id].get('status') != 'verified':
                issues.append('Unknown or unverified reference for ' + key + ': ' + str(ref_id))
        if claim.get('status') == 'supported':
            if claim.get('kind') in {'empirical', 'theoretical'} and not evidence:
                issues.append('Supported empirical/theoretical claim has no evidence: ' + key)
            if claim.get('kind') == 'literature' and not cited:
                issues.append('Supported literature claim has no verified citation: ' + key)
            if claim.get('kind') == 'proposal':
                issues.append('A proposal cannot be marked supported: ' + key)
        for spec in claim.get('numbers', []):
            try:
                actual = source_number(root, spec)
                reported = finite_number(spec['value'])
                tolerance = finite_number(spec.get('tolerance', 1e-6))
                if tolerance < 0:
                    raise ValueError('Tolerance must be nonnegative')
                match = abs(actual - reported) <= tolerance
                numeric_checks.append({'claim': key, 'actual': actual, 'reported': reported, 'matches': match})
                if not match:
                    issues.append('Number mismatch for ' + key)
            except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
                issues.append('Number check for ' + key + ': ' + str(exc))
    manuscript = state.get('manuscript')
    if manuscript:
        path = project_path(root, manuscript)
        if not path.is_file():
            issues.append('Declared manuscript does not exist')
        elif path.suffix.lower() == '.tex':
            # Follow ordinary literal input/include paths. Dynamic TeX macros need manual review.
            pending, visited, texts = [path], set(), []
            while pending:
                item = pending.pop()
                if item in visited:
                    continue
                visited.add(item)
                text = item.read_text(encoding='utf-8-sig')
                text = re.sub(r'(?<!\\)%[^\n]*', '', text)
                texts.append(text)
                for name in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}', text):
                    child = item.parent / name
                    if child.suffix == '':
                        child = child.with_suffix('.tex')
                    child = project_path(root, str(child.relative_to(root)))
                    if child.is_file():
                        pending.append(child)
                    else:
                        issues.append('Missing included TeX file: ' + name)
            text = '\n'.join(texts)
            for keys in re.findall(r'\\(?:cite\w*|autocite|parencite|textcite)\*?(?:\s*\[[^\]]*\])*\s*\{([^}]+)\}', text):
                for key in keys.split(','):
                    key = key.strip()
                    if key not in by_ref or by_ref[key].get('status') != 'verified':
                        issues.append('Unknown or unverified manuscript citation: ' + key)
            warnings.append('TeX parsing covers literal input/include and common cite commands; manually inspect macros and bibliography metadata')
    if level in {'complete', 'submission_candidate'} and (not manuscript or not claims or not primaries):
        issues.append('Complete manuscript needs a file, nonempty claims and a primary claim')
    if level == 'submission_candidate':
        if any(c.get('status') != 'supported' for c in primaries):
            issues.append('A submission candidate has unresolved or refuted primary claims; revise the actual main claim')
        checks = state.get('checks', {})
        for key in CHECKS:
            status = checks.get(key)
            if status == 'passed':
                try:
                    note = project_path(root, state.get('check_evidence', {}).get(key))
                    if not note.is_file():
                        issues.append('Missing check evidence: ' + key)
                except ValueError as exc:
                    issues.append(key + ': ' + str(exc))
            elif status == 'not_applicable' and state.get('not_applicable_reasons', {}).get(key):
                warnings.append('Manual not-applicable justification: ' + key)
            else:
                issues.append('Pending/failed/unjustified check: ' + key)
    issues = list(dict.fromkeys(issues))
    return {
        'structural_consistency_passed': not issues,
        'submission_gate_recorded': level == 'submission_candidate' and not issues,
        'deliverable_level': level, 'claims': len(claims), 'references': len(refs),
        'numeric_checks': numeric_checks, 'issues': issues, 'warnings': warnings,
        'limitation': 'Recorded consistency only. Scientific validity, source authenticity and visual quality require actual review.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--root', required=True)
    init.add_argument('--topic', required=True)
    check = sub.add_parser('audit')
    check.add_argument('--root', required=True)
    args = parser.parse_args()
    try:
        root = pathlib.Path(args.root).resolve()
        result = initialize(root, args.topic) if args.command == 'init' else audit(root)
        code = 0 if args.command == 'init' or result['structural_consistency_passed'] else 1
    except (ValueError, TypeError, KeyError, OSError, json.JSONDecodeError) as exc:
        result, code = {'error': str(exc), 'structural_consistency_passed': False}, 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
