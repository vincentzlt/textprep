from tqdm import tqdm
import collections
import argparse
import os
import subprocess
import sys
import unicodedata
import fileinput


def tok(args):
    pass


def vocab(args):
    pass


def gen_decomp(args):
    pass


def apply_decomp(args):
    pass


def reverse_tok(args):
    pass


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
    parser_gen_decomp = subparsers.add_parser(
        'gen_decomp', help='decomp text into ideographs')
    parser_apply_decomp = subparsers.add_parser(
        'apply_decomp', help='decomp text into ideographs')
    parser_reverse_tok = subparsers.add_parser(
        'reverse_tok', help='reverse tokenization')

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

    parser_gen_decomp.add_argument(
        '-i', '--ids_file', help='cjkvi_ids file', type=str, required=True)
    parser_gen_decomp.add_argument(
        '-l',
        '--decomp_level',
        help='decomp level.',
        choices=['ideo', 'stroke'],
        type=str,
        required=True)
    parser_gen_decomp.add_argument(
        '-c',
        '--circle_char_file',
        help='annotated circled char file.',
        type=str,
        required=True)
    parser_gen_decomp.add_argument(
        '-s',
        '--single_char_file',
        help='annotated single char file.',
        type=str,
        required=True)
    parser_gen_decomp.add_argument(
        '-v', '--vocab_file', help='vocab file.', type=str, required=True)
    parser_gen_decomp.add_argument(
        '-o',
        '--output_file',
        help='output decomp file.',
        type=str,
        default='decomp.txt')
    parser_gen_decomp.set_defaults(func=gen_decomp)

    parser_apply_decomp.add_argument(
        '-i',
        '--input',
        nargs='*',
        help='input file(s).',
        type=str,
        required=True)
    parser_apply_decomp.add_argument(
        '-d',
        '--decomp_file',
        help=
        'decomp file. the decomp vocab should cover vocab in input file(s).',
        type=str,
        required=True)
    parser_apply_decomp.add_argument(
        '-o', '--output', nargs='*', help='output file(s).', type=str)
    parser_apply_decomp.set_defaults(func=apply_decomp)

    parser_reverse_tok.add_argument(
        '-i',
        '--input',
        help='tokenized input file.',
        nargs='*',
        type=str,
        required=True)
    parser_reverse_tok.add_argument(
        '-o', '--output', help='output file.', nargs='*', type=str)
    parser_reverse_tok.add_argument(
        '-m',
        '--method',
        help='tokenize method',
        choices=[
            'jieba', 'mecab', 'kytea', 'moses', 'normalize', 'bpe', 'spm',
            'decomp'
        ],
        type=str,
        required=True)
    parser_reverse_tok.add_argument(
        '-d', '--decomp_file', help='decomp file. (if needed)', type=str)
    parser_reverse_tok.set_defaults(func=reverse_tok)

    return parser


if __name__ == '__main__':
    parser = get_parser()
    cmd_str = 'apply_decomp -h'
    parser.parse_args(cmd_str.split())