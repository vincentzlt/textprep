#!/usr/bin/env python
# coding: utf-8

# In[1]:

import argparse as ap
import collections as cl
import re
import itertools as it
import json

# In[2]:

DUP = '〾'
IDCs = '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'
IDS_FNAME = '../cjkvi-ids/ids.txt'
CIRCLE_FNAME = '../data/circle_char.txt'
SINGLE_FNAME = '../data/single_char.txt'
RE_squarebrackets = re.compile(r'\[[^[]*\]')
RE_IDCs = re.compile(r'[⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻]')

# In[3]:


def _get_d(ds, ideos_set):
    ds = [RE_squarebrackets.sub('', d) for d in ds]
    difference = set(ds).difference(ideos_set)
    while not difference:
        ds = [DUP + d for d in ds]
        difference = set(ds).difference(ideos_set)

    d = difference.pop()
    ideos_set.add(d)

    return d, ideos_set


# In[4]:


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


# In[5]:


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


# In[6]:


def _word_decomp(w, char2ideos, decomp_set):
    decomp = ''.join([char2ideos.get(c, c) for c in w])

    while decomp in decomp_set:
        decomp = DUP + decomp
    decomp_set.add(decomp)

    return decomp, decomp_set


# In[7]:


def _vocab2ideos(vocab, char2ideos):
    vocab_decomps = {}
    decomp_set = set()
    for w in vocab:

        decomp, decomp_set = _word_decomp(w, char2ideos, decomp_set)
        vocab_decomps[w] = decomp

    return vocab_decomps


# In[8]:


def _chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# In[10]:


def main(args):
    if args.level.startswith('ideo'):
        IDS_fnames = [IDS_FNAME, CIRCLE_FNAME]
    elif args.level.startswith('stroke'):
        IDS_fnames = [IDS_FNAME, CIRCLE_FNAME, SINGLE_FNAME]

    char2ideos = _get_char2ideos(IDS_fnames)

    if args.reverse:
        vocab = json.loads(open(args.vocab_fname).read())
    else:
        if not args.idc:
            for c, d in char2ideos.items():
                char2ideos[c] = RE_IDCs.sub('', d)

        if args.level in ['ideo_finest', 'stroke']:
            _recursive_decomp(char2ideos)
        vocab = cl.Counter(
            w for l in open(args.fname) for w in l.strip().split())
        open(args.vocab_fname, 'wt').write((json.dumps(
            ensure_ascii=False, obj=dict(vocab.most_common()), indent=4)))

    vocab2ideos = _vocab2ideos(vocab, char2ideos)

    mapping = {v: k
               for k, v in vocab2ideos.items()
               } if args.reverse else vocab2ideos

    with open(args.output_fname, 'wt') as fout:
        for l in open(args.fname):
            fout.write(' '.join([mapping.get(w, w)
                                 for w in l.strip().split()]) + '\n')


# In[15]:

if __name__ == '__main__':
    parser = ap.ArgumentParser()

    parser.add_argument('fname', type=str, help='the input fname.')
    parser.add_argument(
        '-r',
        '--reverse',
        default=False,
        help=
        'whether to reverse process the input file. If reverse: compose back to normal text file from input fname and vocab fname. Else: do the normal decomposition.'
    )
    parser.add_argument(
        '-v',
        '--vocab_fname',
        type=str,
        help=
        'the vocab fname. in decomp process, vocab file will be generated automatically; in comp process, vocab file must exist to be read from.'
    )
    parser.add_argument(
        '-l',
        '--level',
        choices=['ideo_raw', 'ideo_finest', 'stroke'],
        help='to what level should the decomposition be.')
    parser.add_argument(
        '-i',
        '--idc',
        default=True,
        help='whether to include structual IDCs in the decomp.')
    parser.add_argument(
        '-o', '--output_fname', type=str, help='the output file name.')

    args = parser.parse_args()
    main(args)
