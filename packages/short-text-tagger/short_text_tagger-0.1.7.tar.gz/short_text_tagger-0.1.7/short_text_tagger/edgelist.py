from itertools import combinations, chain
import pandas as pd


class EdgeList:

    def __init__(self, corpus: pd.Series, directed: bool = False, weighted: bool = True):
        
        self.weighted = weighted
        self.directed = directed
        self.corpus: pd.Series = corpus # item: list of words
        self.edgelist: pd.DataFrame = self.generate_edgelist()


    def generate_edgelist(self) -> pd.DataFrame:
        """ provided series of word lists, generate (weighted) edge list"""

        print("Generating edgelist")
        raw_edgelist = self.generate_raw_edgelist()
        if self.weighted:
            weighted_edgelist = self.weight_edgelist(raw_edgelist)
            return weighted_edgelist
        else:
            return raw_edgelist


    def weight_edgelist(self,raw_edgelist) -> pd.DataFrame:
        """ weights raw edgelist """

        raw_edgelist['weight'] = 1
        weighted_edgelist = raw_edgelist.groupby(['source','target']).agg({'weight':'count'}).reset_index()
        return weighted_edgelist 


    def generate_raw_edgelist(self) -> pd.DataFrame:
        """ provided series of word lists, generate unweighted edge list (duplicate edges allowed) """

        if len(self.corpus) == 0:
            # insert warning here
            return pd.DataFrame({"source":[],"target":[]})

        if not self.directed:
            words_combinations_generator = chain.from_iterable(combinations(sorted(words),2) for i, words in self.corpus.iteritems() if len(words)>1)
        else:
            words_combinations_generator = chain.from_iterable(combinations(words,2) for i, words in self.corpus.iteritems() if len(words)>1)
        source,target = zip(*words_combinations_generator)
        raw_edgelist = pd.DataFrame({
                                    'source': list(source),
                                    'target':list(target)
                                    })
        return raw_edgelist
