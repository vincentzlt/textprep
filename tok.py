import argparse
import os
import subprocess
import unicodedata
import sys
from utils import run_cmd, infix, mkdir_if_none, gen_filepair


def to_word(method, in_fname, out_fname):
    if method == 'jieba':
        cmd = 'python -m jieba -d " " {in_file} > {out_file}'
    elif method == 'mecab':
        cmd = 'mecab {in_file} -O wakati > {out_file}'
    elif method == 'kytea':
        cmd = 'kytea -out tok < {in_file} > {out_file}'
    elif method == 'moses':
        cmd = '$HOME/mosesdecoder/scripts/tokenizer/tokenizer.perl < {in_file} > {out_file}'
    else:
        raise ValueError('word tokenizer not supported.')

    print('tokenizing: {} -> {}'.format(in_fname, out_fname), file=sys.stderr)
    run_cmd(cmd.format(in_file=in_fname, out_file=out_fname))


def to_subword(method, vocab_size, in_fnames, out_fnames):
    model_dir = os.path.join(os.path.dirname(in_fnames[0]), 'subword_models')
    model_name = os.path.join(model_dir, '{}_{}'.format(method, vocab_size))
    mkdir_if_none(model_name)
    if not os.path.exists(os.path.join(model_dir, model_name + '.model')):
        # train subword model
        cmd = 'spm_train --input={input} --model_prefix={model_name} --vocab_size={vocab_size} --character_coverage=1.0 --model_type={model_type}'
        run_cmd(
            cmd.format(
                input=in_fnames[0],
                model_name=model_name,
                vocab_size=vocab_size,
                model_type=method))

    cmd = 'spm_encode --model={model} --output_format=piece < {in_file} > {out_file}'
    for in_fname, out_fname in gen_filepair(
            in_fnames, out_fnames, infix_str=os.path.join(method, vocab_size)):
        run_cmd(
            cmd.format(
                model=model_name + '.model',
                in_file=in_fname,
                out_file=out_fname))


def normalize(in_fname, out_fname):
    print('normalizing: {} -> {}'.format(in_fname, out_fname), file=sys.stderr)
    with open(out_fname, 'wt', encoding='utf8') as fout:
        for l in open(in_fname, 'rt', encoding='utf8'):
            fout.write(unicodedata.normalize('NFKD', l))


def tok(args):
    if args.method in ['spm', 'bpe']:
        assert args.vocab_size is not None

    if args.method in ['jieba', 'mecab', 'kytea', 'moses']:
        for in_file, out_file in gen_filepair(
                args.input, args.output, infix_str=args.method):
            to_word(args.method, in_file, out_file)
    elif args.method == 'normalize':
        for in_file, out_file in gen_filepair(
                args.input, args.output, infix_str=args.method):
            normalize(in_file, out_file)
    elif args.method in ['spm', 'bpe']:
        to_subword(args.method, args.vocab_size, args.input, args.output)
    else:
        raise ValueError('tok method not supported.')


if __name__ == '__main__':
    args = argparse.Namespace(
        method='jieba',
        vocab_size='100',
        input=['./test_data/example.cn'],
        output=None,
        extra_options='')

    tok(args)