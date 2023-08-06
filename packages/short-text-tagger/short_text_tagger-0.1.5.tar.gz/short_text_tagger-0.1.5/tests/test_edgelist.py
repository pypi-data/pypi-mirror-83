import sys 
import os
from pathlib import Path 
cwd = str(os.getcwd())
parent_dir = str(Path(os.getcwd()).parent)
sys.path.append(f'{parent_dir}/short_text_tagger/') # if testing from within tests/
sys.path.append(f'{cwd}/short_text_tagger/') # if testing from parent directory

from short_text_tagger.edgelist import EdgeList
import pytest 
import pandas as pd


corpus1 = pd.Series([
    ["store","love","hair","products"],
    [],
    ["communication","key","1"]
])
corpus2 = pd.Series([],dtype=str)


def test_raw_directed_edgelist():

    e1 = EdgeList(corpus1,weighted=False,directed=True)
    e2 = EdgeList(corpus2,weighted=False,directed=True)

    assert e1 is not None, "edge list needs to exist"
    assert e2 is not None, "edge list needs to exist" 

    assert e2.edgelist.equals(pd.DataFrame({"source":[],"target":[]})), "edge lists do not match"
    assert e1.edgelist.equals(pd.DataFrame({
        "source":["store","store","store","love","love","hair","communication","communication","key"],
        "target":["love","hair","products","hair","products","products","key","1","1",]
    })), "edge lists do not match"


def test_raw_undirected_edgelist():

    e1 = EdgeList(corpus1,weighted=False,directed=False)
    e2 = EdgeList(corpus2,weighted=False,directed=False)

    assert e1 is not None, "edge list needs to exist"
    assert e2 is not None, "edge list needs to exist" 

    assert e2.edgelist.equals(pd.DataFrame({"source":[],"target":[]})), "edge lists do not match"
    assert e1.edgelist.equals(pd.DataFrame({
        "source":["hair","hair","hair","love","love","products","1","1","communication"],
        "target":["love","products","store","products","store","store","communication","key","key",]
    })), "edge lists do not match"


