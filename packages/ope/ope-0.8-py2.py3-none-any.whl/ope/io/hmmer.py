#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2019
# File   : hmmer.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 11.12.2019

import re

import pandas as pd

from .base import next_or_raise, convert_dtypes, ChunkParser


class HMMerParser(ChunkParser):
    
    columns = [('target_name', str),
               ('target_accession', str),
               ('tlen', int),
               ('query_name', str),
               ('query_accession', str),
               ('query_len', int),
               ('full_evalue', float),
               ('full_score', float),
               ('full_bias', float),
               ('domain_num', int),
               ('domain_total', int),
               ('domain_c_evalue', float),
               ('domain_i_evalue', float),
               ('domain_score', float),
               ('domain_bias', float),
               ('hmm_coord_from', int),
               ('hmm_coord_to', int),
               ('ali_coord_from', int),
               ('ali_coord_to', int),
               ('env_coord_from', int),
               ('env_coord_to', int),
               ('accuracy', float),
               ('description', str)]

    def __init__(self, filename, **kwargs):
        super(HMMerParser, self).__init__(filename, **kwargs)

    def __iter__(self):
        '''Yields DataFrames of length chunksize from a given
        hmmscan result file.

        HMMER uses 1-based, fully open intervals. Another format of the devil.

        We convert to proper 0-based, half-open intervals.

        Args:
            fn (str): Path to the hmmscan file.
            chunksize (int): Hits per iteration.
        Yields:
            DataFrame: Pandas DataFrame with the hmmscan hits.
        '''

        data = []
        n_entries = 0
        with open(self.filename) as fp:
            for n, ln in enumerate(fp):
                if not ln or ln.startswith('#'):
                    continue

                tokens = ln.split()
                data.append(tokens[:len(self.columns)-1] + \
                            [' '.join(tokens[len(self.columns)-1:])])
                n_entries += 1
                if len(data) >= self.chunksize:
                    yield self._build_df(data)
                    data = []

        if n_entries == 0:
            self.raise_empty()
        if data:
            yield self._build_df(data)

    def _build_df(self, data):
        if not data:
            self.raise_empty()

        df = pd.DataFrame(data, columns=[k for k, _ in self.columns])
        convert_dtypes(df, dict(self.columns))
        # fix the evil coordinate system
        df.hmm_coord_from = df.hmm_coord_from - 1
        df.ali_coord_from = df.ali_coord_from - 1
        df.env_coord_from = df.env_coord_from - 1
        return df
