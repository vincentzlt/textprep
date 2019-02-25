import os
import argparse as ap
import fileinput as fi
import json
import collections as cl
from tqdm import tqdm
import re
import itertools as it

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


def _get_d(ds, ideos_set):
    ds = [RE_squarebrackets.sub('', d) for d in ds]
    difference = set(ds).difference(ideos_set)
    while not difference:
        ds = [DUP + d for d in ds]
        difference = set(ds).difference(ideos_set)

    d = difference.pop()
    ideos_set.add(d)

    return d, ideos_set


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


def vocab(args):
    if os.path.exists(args.vocab) and os.path.getsize(args.vocab):
        vocab = cl.Counter(json.loads(open(args.vocab).read()))
    else:
        vocab = cl.Counter(
            w for l in tqdm(
                it.chain.from_iterable(
                    open(fname, errors='replace') for fname in args.input))
            for w in l.strip().split())

    # print('vocab len: {}'.format(len(vocab)))
    with open(args.vocab, 'wt') as fout:
        fout.write(json.dumps(vocab, indent=4, ensure_ascii=False))

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
    assert (len(vocab2ideos) == len(set(vocab2ideos.values())))
    assert (len(vocab) == len(vocab2ideos))
    # print('saved len {}'.format(len(vocab2ideos)))
    js = json.dumps(vocab2ideos, indent=4, ensure_ascii=False)
    open(args.vocab_decomp, 'wt').write(js)


if __name__ == "__main__":
    vocab_parser = ap.ArgumentParser()
    vocab_parser.add_argument('input', nargs='*', help='input fnames.')
    vocab_parser.add_argument('vocab', help='output vocab fname.')
    vocab_parser.add_argument(
        'vocab_decomp', help='output vocab_decomp fname.')
    vocab_parser.add_argument(
        '--level',
        default='ideo_raw',
        choices=['ideo_raw', 'ideo_finest', 'stroke'],
        help='to what level should the decomposition be.')
    vocab_parser.add_argument(
        '--idc',
        default=True,
        type=_str2bool,
        help='whether to include structual IDCs in the decomp. (yes/no)')

    args = vocab_parser.parse_args()
    print(args)
    vocab(args)