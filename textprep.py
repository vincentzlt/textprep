import argparse

from decomp import main as decomp, _str2bool
from sample import main as sample
from draw import main as draw
from vocab import vocab


def get_parser():
    parser = argparse.ArgumentParser(
        description=
        'tool for analyze (parallel / non-parallel) translation corpus.')
    subparsers = parser.add_subparsers()

    decomp_parser = subparsers.add_parser('decomp')
    decomp_parser.add_argument('input', help='the input fname.')
    decomp_parser.add_argument('output', nargs='?', help='the output fname.')
    decomp_parser.add_argument(
        '--reverse',
        default=False,
        type=_str2bool,
        help=
        'whether to reverse process the input file. If reverse: compose back'
        ' to normal text file from input fname and vocab fname. Else: do the '
        'normal decomposition.')
    decomp_parser.add_argument(
        '--vocab',
        type=str,
        help='the vocab fname. not given, generate vocab from fname.')
    decomp_parser.add_argument(
        '--vocab_decomp',
        type=str,
        help='the vocab_decomp fname. in decomp process, vocab file will be '
        'generated automatically; in comp process, vocab file must exist to '
        'be read from.')
    decomp_parser.add_argument(
        '--level',
        default='ideo_raw',
        choices=['ideo_raw', 'ideo_finest', 'stroke'],
        help='to what level should the decomposition be.')
    decomp_parser.add_argument(
        '--idc',
        default=True,
        type=_str2bool,
        help='whether to include structual IDCs in the decomp. (yes/no)')
    decomp_parser.set_defaults(func=decomp)

    sample_parser = subparsers.add_parser('sample')
    sample_parser.add_argument('src_fname', type=str, help='source file name.')
    sample_parser.add_argument('trg_fname', type=str, help='target file name.')
    sample_parser.add_argument(
        '-n',
        type=int,
        help=
        'num of sampled sentences. should not larger than num of lines in either files.'
    )
    sample_parser.add_argument(
        '-r', type=float, help='the target share token rate for sampling.')
    sample_parser.add_argument(
        '-k', type=int, help='num of sents extracted for each sample step.')
    sample_parser.add_argument(
        '-d',
        '--draw',
        type=str,
        help='if given, draw a graph of sampling process. should end with .html'
    )
    sample_parser.set_defaults(func=sample)

    draw_parser = subparsers.add_parser('draw')
    draw_parser.add_argument(
        'src_fname', type=str, help='the source file name.')
    draw_parser.add_argument(
        'trg_fname', type=str, help='the target file name')
    draw_parser.add_argument(
        '--type',
        type=str,
        choices=['scatter', 'rate', 'both'],
        help='whether to only draw shared tokens')
    draw_parser.add_argument(
        '--output_prefix', default='pref', help='output prefix.')
    sample_parser.add_argument(
        '--src_output',
        type=str,
        default='src_sampled.txt',
        help='source output filename.')
    sample_parser.add_argument(
        '--trg_output',
        type=str,
        default='trg_sampled.txt',
        help='target output filename.')
    draw_parser.set_defaults(func=draw)

    vocab_parser = subparsers.add_parser('vocab')
    vocab_parser.add_argument('input', nargs='*', help='input fnames.')
    vocab_parser.add_argument('vocab', help='output vocab fname.')
    vocab_parser.set_defaults(func=vocab)

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)