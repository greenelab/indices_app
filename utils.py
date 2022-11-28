import glob
import os
import pickle as pkl
from typing import List, Tuple

import pandas as pd


def load_text(file_path: str) -> str:
    """A convenience function for reading in the markdown files used for the site's text"""
    with open(file_path) as in_file:
        return in_file.read()


def extract_heading_name(file_path: str) -> Tuple[str, str]:
    """
    Parse heading names from a file path
    """
    file_base = os.path.basename(file_path)
    both_headings = os.path.splitext(file_base)[0]
    heading1, heading2 = both_headings.split('-')

    return heading1, heading2


def get_heading_names(base_dir='viz_dataframes') -> List[str]:
    """
    Retrieve the names of all MeSH terms we have dataframes for
    """
    result_files = glob.glob(f'{base_dir}/percentiles/*.pkl')

    headings = set()
    for file in result_files:
        heading1, heading2 = extract_heading_name(file)
        headings.add(heading1)
        headings.add(heading2)

    return list(headings)


def get_journal_names(journal_data: pd.DataFrame) -> List[str]:
    """
    Get the names of the commonly used journals for the current pair
    """
    return list(journal_data['journal_title'])


def get_pair_names(heading: str, base_dir='viz_dataframes') -> List[str]:
    """
    Get the names of all headings that have been compared against the given heading
    """
    result_files = glob.glob(f'{base_dir}/percentiles/*{heading}*.pkl')

    pair_headings = set()

    for file in result_files:
        heading1, heading2 = extract_heading_name(file)
        if heading1 == heading:
            pair_headings.add(heading2)
        else:
            pair_headings.add(heading1)
    return list(pair_headings)


def load_percentile_data(heading1:str , heading2: str, base_dir='viz_dataframes') -> pd.DataFrame:
    """
    Load the dataframe containing papers' percentiles and pageranks
    """
    path = f'{base_dir}/percentiles/{heading1}-{heading2}.pkl'
    if os.path.exists(path):
        with open(path, 'rb') as in_file:
            result_df = pkl.load(in_file)
    else:
        path = f'{base_dir}/percentiles/{heading2}-{heading1}.pkl'
        with open(path, 'rb') as in_file:
            result_df = pkl.load(in_file)
    return result_df


def load_journal_data(heading1: str, heading2: str, base_dir='viz_dataframes') -> pd.DataFrame:
    """
    Load the dataframe containing information about journals across fields
    """
    path = f'{base_dir}/journals/{heading1}-{heading2}.pkl'
    if os.path.exists(path):
        with open(path, 'rb') as in_file:
            result_df = pkl.load(in_file)
    else:
        path = f'{base_dir}/journals/{heading2}-{heading1}.pkl'
        with open(path, 'rb') as in_file:
            result_df = pkl.load(in_file)
    return result_df
