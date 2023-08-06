from nltk.corpus import stopwords
import numpy as np


stop_words: set = set(stopwords.words('english'))


def string_to_valid_word_list(string:str) -> list:
    """ creates list of lowercase non-stopwords with no special characters from input string"""

    if not isinstance(string,str) or string == "":
        return []
    else:
        string = lower_case(string)
        string = remove_special_characters(string)
        return split_string(string)


def lower_case(string:str) -> str:
    """ lower case all words """
    assert isinstance(string,str), "cannot lowercase non-string datatype"
    return string.lower()


def remove_special_characters(string:str) -> str:
    """ removing special characters from string """
    assert isinstance(string,str), "cannot remove special characters from non-string datatype"
    string_with_valid_characters = ""
    for character in string:
        if character.isalnum() or character == ' ':
            string_with_valid_characters += character
    return string_with_valid_characters


def split_string(string:str) -> list:
    """ splits string into list of words, removing empty strings and stopwords """
    assert isinstance(string,str), "cannot split non-string datatype"
    word_list = string.split(" ")
    return [word for word in word_list if (word != "" and not word in stop_words)]


