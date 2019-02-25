#!/usr/bin/env python
# coding: utf-8

import argparse as ap
import collections as cl
import re
import itertools as it
import json
import os
import sys
import fileinput as fi


def _str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ap.ArgumentTypeError('Boolean value expected.')


def main(args):
    vocab2ideos = json.loads(open(args.vocab_decomp).read())

    if not args.reverse:
        mapping = vocab2ideos
    else:
        mapping = {v: k for k, v in vocab2ideos.items()}

    fout = open(args.output, 'wt') if args.output else sys.stdout
    for l in fi.input(args.input):
        l_ = ' '.join([mapping[w] for w in l.strip().split()]) + '\n'
        fout.write(l_)
    if fout is not sys.stdout:
        fout.close()


if __name__ == '__main__':
    decomp_parser = ap.ArgumentParser()

    decomp_parser.add_argument('input', help='the input fname.')
    decomp_parser.add_argument('output', nargs='?', help='the output fname.')
    decomp_parser.add_argument(
        '--reverse',
        default=False,
        type=_str2bool,
        help=
        'whether to reverse process the input file. If reverse: compose back'
        ' to normal text file from input fname and vocab fname. Else: do the '
        'normal decomposition.')
    decomp_parser.add_argument(
        '--vocab_decomp',
        type=str,
        help='the vocab_decomp fname. in decomp process, vocab file will be '
        'generated automatically; in comp process, vocab file must exist to '
        'be read from.')
    args = decomp_parser.parse_args()
    print(args)
    main(args)
