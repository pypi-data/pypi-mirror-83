import sys 
import os
from pathlib import Path 
cwd = str(os.getcwd())
parent_dir = str(Path(os.getcwd()).parent)
sys.path.append(f'{parent_dir}/short_text_tagger/') # if testing from within tests/
sys.path.append(f'{cwd}/short_text_tagger/') # if testing from parent directory
print(list(sys.path))
from short_text_tagger.short_text_tagger import generate_topic_distributions_from_corpus
import pytest 
import pandas as pd


def test_smoke():

    short_texts_df = pd.read_csv("data/input.csv")
    df = generate_topic_distributions_from_corpus(short_texts_df)
    print(df)
    assert len(df) == len(short_texts_df)
