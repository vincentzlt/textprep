import argparse

from decomp import main as decomp
from sample import main as sample
from draw import main as draw


def get_parser():
    parser = argparse.ArgumentParser(
        description=
        'tool for analyze (parallel / non-parallel) translation corpus.')
    subparsers = parser.add_subparsers()

    decomp_parser = subparsers.add_parser('decomp')
    decomp_parser.add_argument('fname', type=str, help='the input fname.')
    decomp_parser.add_argument(
        '-r',
        '--reverse',
        default=False,
        help=
        'whether to reverse process the input file. If True: compose back to normal text file from input fname and vocab fname; Else: do the normal decomposition.'
    )
    decomp_parser.add_argument(
        '-v',
        '--vocab_fname',
        type=str,
        help=
        'the vocab fname. in decomp process, vocab file will be generated automatically; in comp process, vocab file must exist to be read from.'
    )
    decomp_parser.add_argument(
        '-l',
        '--level',
        choices=['ideo_raw', 'ideo_finest', 'stroke'],
        help='to what level should the decomposition be.')
    decomp_parser.add_argument(
        '-i',
        '--idc',
        default=True,
        help='whether to include structual IDCs in the decomp.  (yes/no)')
    decomp_parser.add_argument(
        '-o', '--output_fname', type=str, help='the output file name.')
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

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)