from tqdm import tqdm
import collections
import argparse
import os
import subprocess
import sys
import unicodedata
import fileinput
from tok import tok
from vocab import vocab
from decomp import decomp
from reverse import reverse


def get_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        title='subcommands',
        description='perform different preprocessing method on text',
        help='')

    parser_tok = subparsers.add_parser(
        'tok',
        help='process cjkvi-ids data with manually annotated decomp data.')
    parser_vocab = subparsers.add_parser(
        'vocab', help='gen vocab from tokenized files.')
    parser_decomp = subparsers.add_parser(
        'decomp', help='decomp text into ideographs')
    parser_reverse = subparsers.add_parser(
        'reverse', help='reverse tokenization')

    parser_tok.add_argument(
        '-m',
        '--method',
        choices=[
            'jieba', 'mecab', 'kytea', 'moses', 'normalize', 'bpe', 'spm'
        ],
        help='choose tok method',
        required=True)
    parser_tok.add_argument(
        '-v', '--vocab_size', help='vocab size', type=str, default='6000')
    parser_tok.add_argument(
        '-i',
        '--input',
        nargs='*',
        help='input file(s).',
        type=str,
        required=True)
    parser_tok.add_argument(
        '-o', '--output', nargs='*', help='output file(s).', type=str)
    parser_tok.add_argument(
        '-e',
        '--extra_options',
        help='extra cmd option when tokenize the data.',
        type=str,
        default='')
    parser_tok.set_defaults(func=tok)

    parser_vocab.add_argument(
        '-i',
        '--input',
        nargs='*',
        help='input file(s).',
        type=str,
        required=True)
    parser_vocab.add_argument(
        '-o', '--output', help='output vocab file.', type=str)
    parser_vocab.add_argument(
        '-m', '--max_vocab_size', help='maximize vocab size.', default=30000)
    parser_vocab.set_defaults(func=vocab)

    parser_decomp.add_argument(
        '-d', '--ids_file', help='cjkvi_ids file', type=str, required=True)
    parser_decomp.add_argument(
        '-l',
        '--level',
        help='decomp level.',
        choices=['ideo', 'stroke'],
        type=str,
        required=True)
    parser_decomp.add_argument(
        '-c',
        '--circle_char_file',
        help='annotated circled char file.',
        type=str,
        required=True)
    parser_decomp.add_argument(
        '-s',
        '--single_char_file',
        help='annotated single char file.',
        type=str,
        required=True)
    parser_decomp.add_argument(
        '-i',
        '--input',
        nargs='*',
        help='output decomp file.',
        type=str,
        required=True)
    parser_decomp.add_argument(
        '-o', '--output', nargs='*', help='output decomp file.', type=str)
    parser_decomp.set_defaults(func=decomp)

    parser_reverse.add_argument(
        '-i',
        '--input',
        help='tokenized input file.',
        nargs='*',
        type=str,
        required=True)
    parser_reverse.add_argument(
        '-o', '--output', help='output file.', nargs='*', type=str)
    parser_reverse.add_argument(
        '-m',
        '--method',
        help='tokenize method',
        choices=[
            'jieba', 'mecab', 'kytea', 'moses', 'normalize', 'bpe', 'spm',
            'decomp'
        ],
        type=str,
        required=True)
    parser_reverse.add_argument(
        '-d', '--decomp_file', help='decomp file. (if needed)', type=str)
    parser_reverse.set_defaults(func=reverse)

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)