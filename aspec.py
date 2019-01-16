#!/usr/bin/env python
# coding: utf-8

# In[1]:

import itertools as it
import os
import unicodedata as ucd
from tqdm import tqdm as tqdm
import argparse as ap

# In[2]:


def _gen_lines(dname):
    for l in it.chain.from_iterable(
            open(os.path.join(root, fname))
            for root, dirs, fnames in os.walk(dname) for fname in fnames):

        *_, src, trg = l.strip().split(' ||| ')
        yield (src, trg)


# In[5]:


def main(args):
    os.path.exists(args.out_dir) or os.makedirs(args.out_dir)

    if 'jc' in args.aspec_dir.lower():
        SRC = 'ja'
        TRG = 'zh'

    elif 'je' in args.aspec_dir.lower():
        SRC = 'ja'
        TRG = 'en'

    for s in ['train', 'dev', 'test']:
        with open(os.path.join(args.out_dir, '{}.{}'.format(s, SRC)),
                  'wt') as fsrc:
            with open(
                    os.path.join(args.out_dir, '{}.{}'.format(s, TRG)),
                    'wt') as ftrg:
                for src_sent, trg_sent in tqdm(
                        _gen_lines(os.path.join(args.aspec_dir, s)), desc=s):

                    _ = fsrc.write(
                        ucd.normalize(args.norm_type, src_sent) + '\n')
                    _ = ftrg.write(
                        ucd.normalize(args.norm_type, trg_sent) + '\n')


# In[6]:

if __name__ == '__main__':
    parser = ap.ArgumentParser()

    parser.add_argument(
        '--aspec_dir', type=str, help='aspec corpus dir. should contain')
    parser.add_argument('--out_dir', type=str, help='output dir')
    parser.add_argument(
        '--norm_type',
        default='NFKD',
        choices=['NFKD', 'NFKC', 'NFC', 'NFD'],
        help='unicode normalization type; consistant with unicodedata settings. [NFKD]'
    )
    args = parser.parse_args()

    main(args)

# In[ ]:
