import argparse
import collections
from tqdm import tqdm
import os
import fileinput
import sys


def vocab(args):
    if args.output is None:
        dir_name, fname = os.path.split(args.input[0])
        ext = os.path.splitext(fname)[1]
        args.output = os.path.join(dir_name, 'vocab' + ext)
    vocab = collections.Counter(
        w for l in tqdm(fileinput.input(args.input), desc='reading lines')
        for w in l.strip().split())
    with open(args.output, 'wt', encoding='utf8') as fout:
        for idx, (w, count) in enumerate(
                vocab.most_common(args.max_vocab_size)):
            fout.write('{}\t{}\n'.format(w, count))
        print(
            'write {} vocab to {}'.format(idx + 1, args.output),
            file=sys.stderr)


if __name__ == '__main__':
    args = argparse.Namespace(
        input=['./test_data/jieba/example.txt'],
        output=None,
        max_vocab_size=30000)
    vocab(args)