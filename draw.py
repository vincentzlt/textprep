#!/usr/bin/env python
# coding: utf-8

import plotly.offline as py
import plotly.graph_objs as go

import numpy as np
import collections as cl
import itertools as it
from tqdm import tqdm
import os
import argparse as ap


def _draw_scatter(all_vocabs, all_freqs, output_prefix):
    colors = [(s and t) and (s < t and s / t or t / s) or 0
              for s, t in all_freqs]
    colors = [c and np.log(c) or 0 for c in colors]
    trace = go.Scattergl(
        x=[s for s, t in all_freqs],
        y=[t for s, t in all_freqs],
        mode='markers',
        text=all_vocabs,
        marker=dict(color=colors, showscale=True, colorscale='Viridis'))
    layout = go.Layout(
        title='Scatter plot of shared tokens',
        hovermode='closest',
        xaxis=dict(title='src freq', type='log', autorange=True),
        yaxis=dict(title='trg freq', type='log', autorange=True))

    fig = go.Figure(data=[trace], layout=layout)
    py.plot(
        fig, filename='{}_scatter.html'.format(output_prefix), auto_open=False)


def _draw_rate(all_vocabs, all_freqs, output_prefix):
    biases = np.array(
        [(s and t) and (s / t if s > t else t / s) or 0 for s, t in all_freqs])
    freqs = np.array([s + t for s, t in all_freqs])
    hist, bin_edges = np.histogram(
        biases[biases > 0], weights=freqs[biases > 0], bins=int(max(biases)))

    bin_centers = bin_edges[:-1]

    t1 = go.Scatter(
        x=bin_centers,
        y=hist,
        name='num of tokens',
        mode='lines',
        fill='tozeroy')

    share_token_rates = np.cumsum(hist) / sum(freqs)

    t2 = go.Scatter(
        x=bin_centers,
        y=share_token_rates,
        name='share token rates',
        mode='lines',
        yaxis='y2')

    layout = go.Layout(
        title='Shared tokens rates',
        xaxis=dict(title='bias', autorange=True),
        yaxis=dict(title='num of tokens', type='log', autorange=True),
        yaxis2=dict(
            title='accumlative share token rates',
            autorange=True,
            side='right',
            overlaying='y'))
    fig = go.Figure(data=[t1, t2], layout=layout)
    py.plot(
        fig, filename='{}_rate.html'.format(output_prefix), auto_open=False)


def main(args):
    src_freqs = cl.Counter(
        w for l in tqdm(
            open(args.src_fname),
            desc='gen vocab from {}'.format(os.path.basename(args.src_fname)))
        for w in l.strip().split())

    trg_freqs = cl.Counter(
        w for l in tqdm(
            open(args.trg_fname),
            desc='gen vocab from {}'.format(os.path.basename(args.trg_fname)))
        for w in l.strip().split())
    
    if len(src_freqs) * len(trg_freqs) == 0:
        return

    all_vocabs = list(src_freqs.keys() | trg_freqs.keys())
    all_freqs = [(src_freqs.get(v, 0), trg_freqs.get(v, 0))
                 for v in all_vocabs]

    if args.type == 'scatter':
        _draw_scatter(all_vocabs, all_freqs, args.output_prefix)
    elif args.type == 'rate':
        _draw_rate(all_vocabs, all_freqs, args.output_prefix)
    elif args.type == 'both':
        _draw_rate(all_vocabs, all_freqs, args.output_prefix)
        _draw_scatter(all_vocabs, all_freqs, args.output_prefix)


if __name__ == '__main__':
    draw_parser = ap.ArgumentParser()
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
    args = draw_parser.parse_args()

    main(args)
