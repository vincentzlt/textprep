import re
import fileinput
import sys
from tqdm import tqdm
import argparse
import os
from vocab import vocab
from utils import infix, mkdir_if_none


def dup_if_needed(decomp, decomp_set):
    dup_marker = '〾'
    if not decomp in decomp_set:
        return decomp
    else:
        while True:
            decomp = dup_marker + decomp
            if not decomp in decomp_set:
                return decomp


RE_sq_braket = re.compile(r'\[.+?\]')


def read_ids(ids_file, circle_char_file, single_char_file):
    char_decomp = {}
    decomp_set = set()

    for l in tqdm(open(ids_file, 'rt', encoding='utf8'), desc='read ids'):
        if l.startswith('#'): continue

        unicode, c, *decomps = l.strip().split()
        for d in decomps:
            d = RE_sq_braket.sub('', d)
            if not d in decomp_set:
                decomp_set.add(d)
                char_decomp[c] = d
                break
        if not c in char_decomp:
            d = RE_sq_braket.sub('', decomps[0])
            d_bf = d
            d = dup_if_needed(d, decomp_set)
            decomp_set.add(d)
            char_decomp[c] = d

            tqdm.write('\t{}: {} -> {}'.format(c, d_bf, d), file=sys.stderr)

    for l in tqdm(
            fileinput.input((circle_char_file, single_char_file)),
            desc='read circle and single char'):
        c, d = l.strip().split()
        d_bf = d
        if d in decomp_set:
            d = dup_if_needed(d, decomp_set)

        decomp_set.add(d)
        char_decomp[c] = d

        if d_bf != d:
            tqdm.write('\t{}: {} -> {}'.format(c, d_bf, d), file=sys.stderr)

    return char_decomp


def recursive_decomp_(decomp, decomp_dict):
    ret_str = ''
    for d in decomp:
        if d == decomp_dict.get(d, d):
            ret_str += d
        else:
            ret_str += recursive_decomp_(decomp_dict[d], decomp_dict)
    return ret_str


def recursive_decomp(decomp_dict):
    for c, decomp in tqdm(
            decomp_dict.items(), desc='recursive decomp to stroke level'):
        decomp = recursive_decomp_(decomp, decomp_dict)
        decomp_dict[c] = decomp


def check_missing_decomp_info(decomp_dict):
    circle_char = set(list('①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲'))
    single_char = set(list('⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻〾'))

    for c, decomp in tqdm(decomp_dict.items(), desc='check circle char'):
        has_circle_char = any(d in circle_char for d in decomp)
        if has_circle_char:
            tqdm.write('{}: {}'.format(c, decomp), file=sys.stderr)

    for c, decomp in tqdm(decomp_dict.items(), desc='check single char'):
        has_single_char = not any(d in single_char for d in decomp)
        if has_single_char:
            tqdm.write('{}: {}'.format(c, decomp), file=sys.stderr)


def save_decomp(decomp_dict, out_file):
    print('saving decomps to: {}'.format(out_file), file=sys.stderr)
    with open(out_file, 'wt', encoding='utf8') as fout:
        for c, decomp in decomp_dict.items():
            fout.write('{}\t{}\n'.format(c, decomp))


def gen_vocab_decomp(char_decomp, vocab_file):
    vocab = {}
    for l in open(vocab_file, encoding='utf8'):
        v, count = l.strip().split()
        vocab[v] = count

    decomp_set = set()
    word_decomp = {}
    for w in tqdm(vocab, desc='gen vocab decomp'):
        d = ''.join([char_decomp.get(c, c) for c in w])
        if not d in decomp_set:
            decomp_set.add(d)
            word_decomp[w] = d
        else:
            d_bf = d
            d = dup_if_needed(d, decomp_set)
            decomp_set.add(d)
            word_decomp[w] = d
            tqdm.write('\t{}: {} -> {}'.format(w, d_bf, d), file=sys.stderr)
    return word_decomp


def decomp(args):
    dir_name, fname = os.path.split(args.input[0])
    f_basename, ext = os.path.splitext(fname)
    vocab_fname = os.path.join(dir_name, 'vocab' + ext)
    decomp_fname = os.path.join(dir_name, 'decomp' + ext)

    if not os.path.exists(vocab_fname):
        vocab_args = argparse.Namespace(
            input=args.input, output=vocab_fname, max_vocab_size=30000)
        vocab(vocab_args)

    char_decomp = read_ids(
        ids_file=args.ids_file,
        circle_char_file=args.circle_char_file,
        single_char_file=args.single_char_file)
    assert len(char_decomp.values()) == len(set(char_decomp.values()))
    print('num of decomps: {}'.format(len(char_decomp)), file=sys.stderr)

    check_missing_decomp_info(char_decomp)

    if args.level == 'stroke':
        recursive_decomp(char_decomp)

    word_decomp = gen_vocab_decomp(char_decomp, vocab_fname)

    save_decomp(word_decomp,
                os.path.join(dir_name, args.level + '_decomp' + ext))

    for in_fname in args.input:
        out_fname = infix(in_fname, args.level)
        mkdir_if_none(out_fname)
        with open(out_fname, 'wt', encoding='utf8') as fout:
            for l in tqdm(
                    open(in_fname, 'rt', encoding='utf8'),
                    desc='decomp to {}'.format(out_fname)):
                fout.write(' '.join([word_decomp[w]
                                     for w in l.split()]) + '\n')


if __name__ == '__main__':
    args = argparse.Namespace(
        input=['./test_data/jieba/example.txt'],
        output=None,
        ids_file='./cjkvi-ids/ids.txt',
        circle_char_file='./data/circle_char.txt',
        single_char_file='./data/single_char.txt',
        level='stroke')
    decomp(args)
