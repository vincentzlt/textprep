import os
import argparse
from utils import infix, mkdir_if_none
from tqdm import tqdm


def rm_space(line):
    return ''.join(line.split())


def reverse_spm(line):
    return rm_space(line).replace('▁', ' ')


def reverse_decomp(line, reverse_decomp_dict):
    return ' '.joint([reverse_decomp_dict.get(w, w) for w in line.split()])


def reverse(args):
    if args.method in ['jieba', 'mecab', 'kytea', 'moses']:
        reverse_func = rm_space
    elif args.method in ['bpe', 'spm']:
        reverse_func = reverse_spm
    elif args.method in ['decomp']:
        reverse_func = reverse_decomp
    else:
        raise ValueError('method not supported.')

    for in_fname in args.input:
        out_fname = infix(in_fname, 'reverse_' + args.method)
        mkdir_if_none(out_fname)
        with open(out_fname, 'wt', encoding='utf8') as fout:
            for l in tqdm(
                    open(in_fname, 'rt', encoding='utf8'),
                    desc='reverse {} to {}'.format(args.method, out_fname)):
                fout.write(reverse_func(l) + '\n')


if __name__ == '__main__':
    args = argparse.Namespace(
        input=['./test_data/jieba/example.txt'],
        output=None,
        method='jieba',
        decomp_file='./test_data/jieba/stroke_decomp.txt')
    reverse(args)