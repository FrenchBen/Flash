#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import json
import glob

if '-h' in sys.argv or '--help' in sys.argv:
    print('usage:', file=sys.stderr)
    print('echo GET http://localhost:8080/ | %s' % sys.argv[0], file=sys.stderr)
    sys.exit(1)

prefix = ''
if '-p' in sys.argv or '--prefix' in sys.argv:
    if '-p' == sys.argv[1]:
        prefix = '%s-' % sys.argv[2]

target = sys.stdin.read().strip()

# Log-spaced rates (each ca. +25% (+1dB) of the previous, covering 1/sec to 100k/sec)
rates = [10.0 ** (i / 10.0) for i in range(50)]

# Log-spaced buckets (each ca. +25% (+1dB) of the previous, covering <1us to >10s)
buckets = [0] + [1e3 * 10.0 ** (i / 10.0) for i in range(71)]

# Clear previous runs
files = glob.glob('results/*.bin')
for f in files:
    os.remove(f)

# Run vegeta attack
for rate in rates:
    filename='results/results_%i.bin' % (1000*rate)
    if not os.path.exists(filename):
        cmd = 'vegeta attack -duration 5s -rate %i/1000s -output %s' % (1000*rate, filename)
        print(cmd, file=sys.stderr)
        subprocess.run(cmd, shell=True, input=target, encoding='utf-8')
        time.sleep(5)

# Run vegeta report, and extract data for gnuplot
with open('%sresults_latency.txt' % prefix, 'w') as out_latency, \
     open('%sresults_success.txt' % prefix, 'w') as out_success:

    for rate in rates:
        filename='results/results_%i.bin' % (1000*rate)
        cmd = 'vegeta report -type=json -buckets \'%s\' %s' \
            % ("[%s]" % ",".join("%ins" % bucket for bucket in buckets), filename)
        print(cmd, file=sys.stderr)
        result = json.loads(subprocess.check_output(cmd, shell=True))

        # (Request rate, Response latency) -> (Fraction of responses)
        for latency, count in result['buckets'].items():
            latency_nsec = float(latency)
            fraction = count / sum(result['buckets'].values()) * result['success']
            print(rate, latency_nsec, fraction, file=out_latency)
        print(file=out_latency)

        # (Request rate) -> (Success rate)
        print(rate, result['success'], file=out_success)

print(f'# wrote {prefix}results_latency.txt and {prefix}results_success.txt', file=sys.stderr)


# Visualize with gnuplot (PNG)
cmd = 'gnuplot -e "set term png size 1280, 800" ramp-requests.plt > %sresult.png' % prefix
print(cmd, file=sys.stderr)
subprocess.run(cmd, shell=True)

# Visualize with gnuplot (default, likely a UI)
# cmd = 'gnuplot -persist ramp-requests.plt'
# print(cmd, file=sys.stderr)
# subprocess.run(cmd, shell=True)