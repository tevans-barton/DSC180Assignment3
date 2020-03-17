#!/usr/bin/env python

import sys
import json
import shutil
import pandas as pd
import os
sys.path.append('src')
sys.path.append('src/data')
sys.path.append('src/processing')
from etl import get_data
import cleaning
import calculations

DATA_PARAMS = 'config/data-params.json'
TEST_PARAMS = 'config/test-params.json'
directories = ['data/raw', 'data/test']


def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)
    return param


def main(targets):
    if 'test-project' in targets:
        targets.append('test')
        targets.append('transform')

    if 'clean' in targets:
        shutil.rmtree('data/raw',ignore_errors=True)
        shutil.rmtree('data/out',ignore_errors=True)
        shutil.rmtree('data/test',ignore_errors=True)
    
    if 'data' in targets:
        cfg = load_params(DATA_PARAMS)
        get_data(**cfg)

    if 'test' in targets:
        cfg = load_params(TEST_PARAMS)
        get_data(**cfg)

    if 'transform' in targets:
        for directory in directories:
            if not os.path.exists(directory):
                continue
            for filename in os.listdir(directory):
                if filename.endswith("csv"):
                    if '2018' in filename:
                        temp_df = cleaning.clean_2018_2019(directory + '/' + filename)
                        df = calculations.get_inner_twilight_period(temp_df)
                        calculations.veil_of_darkness(df, 2018, notebook = False)
                    else:
                        year = int(filename[0:4])
                        temp_df = cleaning.clean_2014_2017(directory + '/' + filename)
                        df = calculations.get_inner_twilight_period(temp_df)
                        calculations.veil_of_darkness(df, year, notebook = False)
                continue
            else:
                continue
    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)


    