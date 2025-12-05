#!/usr/bin/env python3

import argparse
import pandas

parser = argparse.ArgumentParser()
parser.add_argument('--in_csvs', required=True, nargs='*')
parser.add_argument('--out_csv', required=True)
args = parser.parse_args()

outcsv = pandas.read_csv(args.in_csvs[0])

for csv in args.in_csvs[1:]:
    csvn = pandas.read_csv(csv)
    outcsv = pandas.concat([outcsv, csvn])

outcsv.to_csv(args.out_csv, header=True, index=False)

