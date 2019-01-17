#!/usr/bin/env python
# coding: utf-8

import os
import sys

import numpy as np
import collections as cl
import argparse as ap
from tqdm import tqdm as tqdm
import time

import plotly.offline as py
import plotly.graph_objs as go


def _pool(fname):
    sents = {
        idx: cl.Counter(l.strip().split())
        for idx, l in enumerate(open(fname))
    }
    total = np.array([sum(sents[idx].values()) for idx in range(len(sents))])
    shared = np.array([0] * len(sents))
    mask = np.array([False] * len(sents))

    return dict(sents=sents, total=total, shared=shared, mask=mask)


def _sample_k(pool, k, large=True):
    shared = np.ma.array(pool['shared'] / pool['total'], mask=pool['mask'])

    return shared.argsort(fill_value=0)[-k:] if large else shared.argsort(
        fill_value=np.inf)[:k]


def _shared_vocab(src_sents, trg_sents):
    src_vocab = set.union(*[set(s.keys()) for s in src_sents.values()])
    trg_vocab = set.union(*[set(s.keys()) for s in trg_sents.values()])

    return src_vocab & trg_vocab


def _update_pool(pool, idxs, vocab):
    # change mask
    for idx in idxs:
        pool['mask'][idx] = True

    # mark shared vocab
    for idx in pool['sents']:
        for v in vocab:
            if v in pool['sents'][idx]:
                pool['shared'][idx] += pool['sents'][idx].pop(v)


def _r(src_pool, trg_pool):
    src_shared = np.ma.array(src_pool['shared'], mask=~src_pool['mask'])
    src_total = np.ma.array(src_pool['total'], mask=~src_pool['mask'])

    trg_shared = np.ma.array(trg_pool['shared'], mask=~trg_pool['mask'])
    trg_total = np.ma.array(trg_pool['total'], mask=~trg_pool['mask'])

    return (src_shared.sum() + trg_shared.sum()) / (
        src_total.sum() + trg_total.sum())


def _draw(rs, steps, vocabs, filename):
    t_r = go.Scatter(x=steps, y=rs, yaxis='y2', name='token sharing rate')
    t_num_vocabs = go.Bar(
        y=[len(v) for v in vocabs], x=steps, text=vocabs, name='vocabs')
    data = [t_r, t_num_vocabs]
    layout = go.Layout(
        title='token rate sampling progress',
        yaxis=dict(title='num of vocabs', type='log'),
        yaxis2=dict(
            title='sampled token sharing rate', overlaying='y', side='right'))
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename, auto_open=False)


def _sample(src_pool, trg_pool, n, r, k=1, draw=''):
    src_sents = {
        idx: src_pool['sents'][idx]
        for idx in range(len(src_pool['mask'])) if src_pool['mask'][idx]
    }
    trg_sents = {
        idx: trg_pool['sents'][idx]
        for idx in range(len(trg_pool['mask'])) if trg_pool['mask'][idx]
    }
    shared_vocab = _shared_vocab(
        src_sents, trg_sents) if len(src_sents) and len(trg_sents) else set()
    shared_vocab_step = set()
    current_r = 0

    t = tqdm(
        total=n, file=sys.stdout, initial=src_pool['mask'].sum(), ncols=100)

    if draw:
        d_rs = [current_r]
        d_steps = [t.n]
        d_shared_vocabs = [shared_vocab]

        _draw(d_rs, d_steps, d_shared_vocabs, filename=draw)

    while not (t.n > n and abs(current_r - r) < 0.001) and t.n < min(
            len(src_pool['sents']), len(src_pool['sents'])):

        large = True if current_r < r else False
        src_idxs = _sample_k(src_pool, k, large)
        trg_idxs = _sample_k(trg_pool, k, large)

        src_sents = {idx: src_pool['sents'][idx] for idx in src_idxs}
        trg_sents = {idx: trg_pool['sents'][idx] for idx in trg_idxs}
        #         pdb.set_trace()
        shared_vocab_step = _shared_vocab(src_sents, trg_sents)

        shared_vocab_step = shared_vocab_step.difference(shared_vocab)
        shared_vocab.update(shared_vocab_step)

        _update_pool(src_pool, src_idxs, shared_vocab_step)
        _update_pool(trg_pool, trg_idxs, shared_vocab_step)
        #         pdb.set_trace()

        current_r = _r(src_pool, trg_pool)
        d_rs.append(current_r)
        d_steps.append(t.n)
        d_shared_vocabs.append(shared_vocab_step)

        if t.n / k % 20 == 0:
            _draw(d_rs, d_steps, d_shared_vocabs, filename=draw)

        desc = 'v: {} | new v: {} | r: {:.2%} '.format(
            len(shared_vocab), len(shared_vocab_step), current_r)
        t.desc = desc

        t.update(k)

    t.close()


def _save(pool, in_fname, out_fname):
    with open(out_fname, 'wt') as fout:
        for idx, l in enumerate(open(in_fname)):
            if pool['mask'][idx]:
                fout.write(l)


def main(args):
    src_pool = _pool(args.src_fname)
    trg_pool = _pool(args.trg_fname)

    _sample(src_pool, trg_pool, args.n, args.r, args.k, draw=args.draw)

    _save(src_pool, args.src_fname, args.src_output)
    _save(trg_pool, args.trg_fname, args.trg_output)


if __name__ == '__main__':
    sample_parser = ap.ArgumentParser()

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
    args = sample_parser.parse_args()

    main(args)
