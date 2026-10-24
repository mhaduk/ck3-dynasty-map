#!/usr/bin/env python3
"""Generate a finite two-shade palette from an explicit ordered RGB-pair roster."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def shades(c1, c2):
    mix = [0.75 * a + 0.25 * b for a, b in zip(c1, c2)]
    peak = max(mix)
    if peak < 40:
        dark = [40, 40, 40] if peak == 0 else [math.floor(x * 40 / peak + .5) for x in mix]
    else:
        dark = [math.floor(x + .5) for x in mix]
    light = [math.floor(x + .35 * (255 - x) + .5) for x in dark]
    return dark, light


def build(roster):
    if roster.get('schema') != 'dynmap-r016-palette-input/1':
        raise ValueError('unsupported roster schema')
    pairs = roster.get('complete_pairs')
    missing = roster.get('missing_pair_ids')
    if not isinstance(pairs, list) or not isinstance(missing, list):
        raise ValueError('complete_pairs and missing_pair_ids must be arrays')
    ids = []
    rows = []
    for item in pairs:
        pair_id = item['pair_id']
        c1, c2 = item['color1_rgb'], item['color2_rgb']
        if type(pair_id) is not int or pair_id < 1 or pair_id > 88:
            raise ValueError('pair_id outside frozen range')
        if pair_id in ids:
            raise ValueError('duplicate pair_id')
        for vector in (c1, c2):
            if not isinstance(vector, list) or len(vector) != 3 or any(type(v) not in (int, float) or not 0 <= v <= 255 for v in vector):
                raise ValueError('RGB values must be three numeric bytes')
        ids.append(pair_id)
        center = [math.floor(v + .5) for v in c1 + c2]
        dark, light = shades(c1, c2)
        rows.append({'pair_id':pair_id,'rgb6_center':center,'dark':dark,'light':light})
    missing_ids = sorted(missing)
    if len(ids) != 76 or len(set(missing_ids)) != 12 or set(ids) & set(missing_ids) or len(set(ids + missing_ids)) != 88:
        raise ValueError('roster must contain 76 complete and 12 distinct missing pairs')
    digest = roster.get('source_roster_sha256')
    if not isinstance(digest, str) or len(digest) != 64:
        raise ValueError('source roster SHA-256 is required')
    return {'schema':'dynmap-r016-palette/1','source_roster_sha256':digest,
            'pair_count':88,'complete_pair_count':76,'missing_color2_count':12,
            'matching':{'channels':6,'inclusive_tolerance':5,'boxes_disjoint':True},
            'dark_formula':'75% color1 + 25% color2; maximum-channel floor 40/255 only when darker; zero maps to 40/40/40; half-up byte rounding',
            'light_formula':'dark + 35% toward white; half-up byte rounding',
            'missing_pair_ids':missing_ids,'unknown_fallback':{'dark':[25,105,50],'light':[145,220,150]},
            'rows':sorted(rows,key=lambda row:row['pair_id'])}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    payload=json.loads(args.input.read_text())
    result=build(payload)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'pairs':result['pair_count'],'complete':len(result['rows']),'missing':len(result['missing_pair_ids']),'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}))

if __name__=='__main__':
    main()
