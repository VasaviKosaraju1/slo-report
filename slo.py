"""Summarize an explicit observation window; no live telemetry required."""
import argparse
import json
import math
from pathlib import Path
import sys


def finite(value, name):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
        raise ValueError(name+' must be a finite number')
    return value


def report(config):
    target=finite(config['availability_target'],'availability_target')
    threshold=finite(config['latency_threshold_ms'],'latency_threshold_ms')
    if not 0 < target < 1 or threshold < 0:
        raise ValueError('target must be between zero and one; latency threshold must be nonnegative')
    rows=config['observations']
    if not rows: raise ValueError('observation window is empty')
    latencies=[];failures=0;ids=set()
    for row in rows:
        identifier=row['request_id']
        if not isinstance(identifier,str) or not identifier or identifier in ids:
            raise ValueError('request_id must be a unique nonempty string')
        ids.add(identifier)
        status=row['status']
        if isinstance(status,bool) or not isinstance(status,int) or not 100 <= status <= 599:
            raise ValueError('status must be an HTTP status integer')
        latency=finite(row['latency_ms'],'latency_ms')
        if latency < 0: raise ValueError('latency cannot be negative')
        latencies.append(latency)
        failures += status >= 500
    count=len(rows);allowed=count*(1-target)
    ordered=sorted(latencies)
    percentile=lambda p: ordered[math.ceil(p*count)-1]
    return {'requests':count,'failed_requests':failures,'availability':(count-failures)/count,
            'availability_target':target,'allowed_failed_requests':round(allowed,6),
            'error_budget_remaining_requests':round(allowed-failures,6),
            'error_budget_consumed_ratio':failures/allowed,
            'availability_met':failures <= allowed + 1e-12,
            'latency_threshold_ms':threshold,
            'requests_within_latency_ratio':sum(v<=threshold for v in latencies)/count,
            'p50_latency_ms':percentile(.50),'p95_latency_ms':percentile(.95)}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('window');a=p.parse_args()
    try: result=report(json.loads(Path(a.window).read_text()))
    except (ValueError,KeyError,TypeError,OSError) as e:
        print(json.dumps({'error':str(e)}),file=sys.stderr);return 2
    print(json.dumps(result,indent=2));return 0 if result['availability_met'] else 1

if __name__=='__main__': sys.exit(main())
