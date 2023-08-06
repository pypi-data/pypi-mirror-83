import sys 
import os
from pathlib import Path 
cwd = str(os.getcwd())
parent_dir = str(Path(os.getcwd()).parent)
sys.path.append(f'{parent_dir}/short_text_tagger/') # if testing from within tests/
sys.path.append(f'{cwd}/short_text_tagger/') # if testing from parent directory

from short_text_tagger import text
from nltk.corpus import stopwords
import pytest

stop_words: set = set(stopwords.words('english'))

def test_lower_case(): 
    s1 = "abcdefgh"
    s2 = "ABCDEFGH"
    s3 = "12345"
    s4 = " "

    assert text.lower_case(s1) == s1 
    assert text.lower_case(s2) == s1
    assert text.lower_case(s3) == s3
    assert text.lower_case(s4) == s4

def test_remove_special_characters():
    s1 = "abcd$%^"
    s2 = "^&%$#~"
    s3 = " "
    s4 = "I went shopp&^%**ing"
    assert text.remove_special_characters(s1) == "abcd"
    assert text.remove_special_characters(s2) == ""
    assert text.remove_special_characters(s3) == " "
    assert text.remove_special_characters(s4) == "I went shopping"
     


def test_split_string():
    s1 = ""
    s2 = "Go find the treasure"
    s3 = "and but or "

    assert text.split_string(s1) == []
    assert text.split_string(s2) == ['Go', 'find', 'treasure']
    assert text.split_string(s3) == []


def test_string_to_valid_word_list():
    s1 = "I went to the store to buy coffee"
    s2 = ""
    s3 = "     "
    s4 = "Sentence with CAPITALIZATION and special %^&*%$ !!!"

    assert text.string_to_valid_word_list(s1) == ["went","store","buy","coffee"]
    assert text.string_to_valid_word_list(s2) ==  []
    assert text.string_to_valid_word_list(s3) == []
    assert text.string_to_valid_word_list(s4) == ["sentence","capitalization","special"]