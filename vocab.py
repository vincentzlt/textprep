import os
import argparse as ap
import fileinput as fi
import json
import collections as cl
from tqdm import tqdm


def vocab(args):
    vocab = cl.Counter(
        w for l in tqdm(fi.input(args.input)) for w in l.strip().split())
    with open(args.vocab, 'wt') as fout:
        fout.write(json.dumps(vocab, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    vocab_parser = ap.ArgumentParser()
    vocab_parser.add_argument('input', nargs='*', help='input fnames.')
    vocab_parser.add_argument('vocab', help='output vocab fname.')
    args = vocab_parser.parse_args()
    print(args)
    vocab(args)