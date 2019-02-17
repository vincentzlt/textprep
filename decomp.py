#!/usr/bin/env python
# coding: utf-8

import argparse as ap
import collections as cl
import re
import itertools as it
import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DUP = '〾'
IDCs = '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'
IDS_FNAME = os.path.join(CURRENT_DIR, 'cjkvi-ids', 'ids.txt')
CIRCLE_FNAME = os.path.join(CURRENT_DIR, 'data', 'circle_char.txt')
SINGLE_FNAME = os.path.join(CURRENT_DIR, 'data', 'single_char.txt')
RE_squarebrackets = re.compile(r'\[[^[]*\]')
RE_IDCs = re.compile(r'[⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻]')


def _str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ap.ArgumentTypeError('Boolean value expected.')


def _get_d(ds, ideos_set):
    ds = [RE_squarebrackets.sub('', d) for d in ds]
    difference = set(ds).difference(ideos_set)
    while not difference:
        ds = [DUP + d for d in ds]
        difference = set(ds).difference(ideos_set)

    d = difference.pop()
    ideos_set.add(d)

    return d, ideos_set


def _get_char2ideos(fnames):
    char2ideos = {}
    ideos_set = set()

    for l in it.chain.from_iterable(open(fname) for fname in fnames):
        if not l.startswith('#'):
            if l.startswith('U'):
                u, c, *ds = l.strip().split()
            else:
                c, *ds = l.strip().split()

            char2ideos[c], ideos_set = _get_d(ds, ideos_set)
    return char2ideos


def _recursive_decomp(char2ideos):
    ideos_set = set()

    for c, d in char2ideos.items():
        while True:
            new_d = ''.join([char2ideos.get(c_, c_) for c_ in d])
            if new_d == d:
                break
            else:
                d = new_d

        while d in ideos_set:
            d = DUP + d
        char2ideos[c] = d
        ideos_set.add(d)


def _word_decomp(w, char2ideos, decomp_set):
    decomp = ''.join([char2ideos.get(c, c) for c in w])

    while decomp in decomp_set:
        decomp = DUP + decomp
    decomp_set.add(decomp)

    return decomp, decomp_set


def _vocab2ideos(vocab, char2ideos):
    vocab_decomps = {}
    decomp_set = set()
    for w in vocab:

        decomp, decomp_set = _word_decomp(w, char2ideos, decomp_set)
        vocab_decomps[w] = decomp

    return vocab_decomps


def _chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def main(args):
    if args.vocab:
        vocab = cl.Counter(json.loads(open(args.vocab).read()))
    else:
        vocab = cl.Counter(
            w for l in open(args.input) for w in l.strip().split())

    if args.vocab_decomp and args.reverse:
        vocab2ideos = json.loads(open(args.vocab_decomp).read())
    else:
        if args.level.startswith('ideo'):
            IDS_fnames = [IDS_FNAME, CIRCLE_FNAME]
        elif args.level.startswith('stroke'):
            IDS_fnames = [IDS_FNAME, CIRCLE_FNAME, SINGLE_FNAME]

        char2ideos = _get_char2ideos(IDS_fnames)

        if not args.idc:
            for c, d in char2ideos.items():
                char2ideos[c] = RE_IDCs.sub('', d)

        if args.level in ['ideo_finest', 'stroke']:
            _recursive_decomp(char2ideos)

        vocab2ideos = _vocab2ideos(vocab, char2ideos)
        js = json.dumps(vocab2ideos, indent=4, ensure_ascii=False)
        open(args.vocab_decomp, 'wt').write(js)

    if not args.reverse:
        mapping = vocab2ideos
    else:
        mapping = {v: k for k, v in vocab2ideos.items()}

    fout = open(args.output, 'wt') if args.output else sys.stdout
    for l in open(args.input):
        l_ = ' '.join([mapping.get(w, w) for w in l.strip().split()]) + '\n'
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
        '--vocab',
        type=str,
        help='the vocab fname. not given, generate vocab from fname.')
    decomp_parser.add_argument(
        '--vocab_decomp',
        type=str,
        help='the vocab_decomp fname. in decomp process, vocab file will be '
        'generated automatically; in comp process, vocab file must exist to '
        'be read from.')
    decomp_parser.add_argument(
        '--level',
        default='ideo_raw',
        choices=['ideo_raw', 'ideo_finest', 'stroke'],
        help='to what level should the decomposition be.')
    decomp_parser.add_argument(
        '--idc',
        default=True,
        type=_str2bool,
        help='whether to include structual IDCs in the decomp. (yes/no)')

    args = decomp_parser.parse_args()
    print(args)
    main(args)
