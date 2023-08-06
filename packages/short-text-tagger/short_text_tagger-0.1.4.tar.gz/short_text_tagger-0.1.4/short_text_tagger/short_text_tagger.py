import nltk
import pandas as pd
from short_text_tagger.text import string_to_valid_word_list
from edgelist import EdgeList
from nsbm import NSBM
from collections import defaultdict
import sys

nltk.download('stopwords')


def cleaned_texts_df_from_data(short_texts_df:pd.DataFrame) -> pd.DataFrame:
    """ Returns cleaned short texts dataframe 

    Parameters
    ----------
    short_texts_df : pd.DataFrame
        "id" and "text" columns

    Returns
    -------
    short_texts_df : pd.DataFrame
        additional "words" column
    """

    assert 'id' in short_texts_df.columns, "'id' is a required column name for this analysis" 
    assert 'text' in short_texts_df.columns, "'text' is a required column name for this analysis" 
    assert len(short_texts_df) > 0, "Need at least one short text for this analysis"

    short_texts_df = short_texts_df[['id','text']]
    short_texts_df['words'] = short_texts_df['text'].apply(lambda text: string_to_valid_word_list(text)) 
    return short_texts_df



def word_to_block_dict(edgelist: EdgeList, block_level: int) -> dict:
    """ Returns a word to topic (block) map for every word in edgelist by fitting an NSBM 
        from the edgelist and assigning each node to its community

    Parameters
    ----------
    edgelist : EdgeList

    Returns
    -------
    dict [word:block] 
        
    """
    nsbm = NSBM(edgelist,block_level = block_level)
    nsbm.fit()
    return {word: nsbm.block_index_to_block_name_dict[nsbm.get_block_from_node(i)] 
            for word, i in nsbm.node_name_to_node_index.items()}



def assign_text_probabilities(short_texts_df: pd.DataFrame, word_to_block_dict_list: list) -> pd.DataFrame:
    """ Assigns topic probabilities to short_texts_df 

    Parameters
    ----------
    short_texts_df : pd.DataFrame
        "id", "text", and "words" columns
    word_to_block_dict_list: List[Dict]
        list of word to block mappings

    Returns
    -------
    short_texts_df : pd.DataFrame
        additional columns of form "topic_prob__<topic>"
    """

    # initializing dict of topic probabilities for each short text
    text_topic_probabilities = {row['id']: defaultdict(int) for i,row in short_texts_df.iterrows()}
    topics_seen = set()
    for word_to_block in word_to_block_dict_list:
        topics_seen = topics_seen.union(set(word_to_block.values()))

    # for each text, get probabilities of topic memberships
    for _,row in short_texts_df.iterrows():
        for word in row['words']:
            for word_to_block in word_to_block_dict_list:
                block = word_to_block[word]
                text_topic_probabilities[row['id']][block] += 1/(len(word_to_block_dict_list)*len(row['words']))

    for topic in topics_seen:
        short_texts_df[f'topic_prob__{topic}'] = short_texts_df['id'].apply(lambda id: text_topic_probabilities[id][topic] if topic in text_topic_probabilities[id].keys() else 0) 
  
    return short_texts_df


def generate_topic_distributions_from_corpus(short_texts_df:pd.DataFrame, 
                                             iterations:int = 5, 
                                             weighted:bool = True,
                                             directed:bool = False,
                                             block_level = 2) -> pd.DataFrame: 


    short_texts_df = cleaned_texts_df_from_data(short_texts_df)
    edgelist = EdgeList(corpus = short_texts_df['words'], directed = directed, weighted = weighted)
    word_to_block_dict_list = [word_to_block_dict(edgelist,block_level) for _ in range(iterations)]
    short_texts_df = assign_text_probabilities(short_texts_df,word_to_block_dict_list)
    return short_texts_df


