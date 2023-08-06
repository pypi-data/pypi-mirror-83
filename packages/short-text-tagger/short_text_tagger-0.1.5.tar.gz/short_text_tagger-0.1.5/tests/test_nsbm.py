import sys 
import os
from pathlib import Path 
cwd = str(os.getcwd())
parent_dir = str(Path(os.getcwd()).parent)
sys.path.append(f'{parent_dir}/short_text_tagger/') # if testing from within tests/
sys.path.append(f'{cwd}/short_text_tagger/') # if testing from parent directory
import pandas as pd 
import pytest 
from edgelist import EdgeList
from nsbm import NSBM

corpus1 = pd.Series([
    ["store","love","hair","products"],
    [],
    ["communication","key","1"]
])
e1 = EdgeList(corpus1,weighted=True,directed=False)

def test_graph_and_nsbm_creation_naive():
    nsbm = NSBM(e1,block_level = 2)
    assert nsbm.g is not None 
    assert len(nsbm.g.get_vertices()) == 7, "the graph doesn't have the correct number of vertices"
    assert len(nsbm.g.get_edges()) == 9, "the graph doesn't have the correct number of edges"
    nsbm.fit()
    assert nsbm.state is not None, "the NSBM state needs to exist after fit() is called"