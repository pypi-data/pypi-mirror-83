=================
short_text_tagger
=================


.. image:: https://img.shields.io/pypi/v/short_text_tagger.svg
        :target: https://pypi.python.org/pypi/short_text_tagger

.. image:: https://img.shields.io/travis/JohnAnthonyBowllan/short_text_tagger.svg
        :target: https://travis-ci.com/JohnAnthonyBowllan/short_text_tagger

.. image:: https://readthedocs.org/projects/short-text-tagger/badge/?version=latest
        :target: https://short-text-tagger.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




short_text_tagger generates topic distributions for all texts in a corpus.


* Free software: MIT license

Installation
------------
``pip install short_text_tagger``

Usage 
--------
If you have graph-tool installed and want to use its community detection functionality to generate topics, then
import ``short_text_tagger.generate_topic_distributions_from_corpus`` into your project. This function
expects a pandas DataFrame with columns ``id`` and ``text``.

If you don't have graph-tool installed or want to substitute other community detection algorithms, then 
you have the option of importing ``cleaned_texts_df_from_data`` from ``short_text_tagger`` for text preprocessing 
and adding a required ``words`` column to the aforementioned DataFrame. After, you can import ``assign_text_probabilities``, 
which expects the input DataFrame with an added ``words`` column and a list of dictionaries (word to topic mappings)
and returns the same DataFrame with appended topic probability columns. The hook is the creation of the list of word to 
topic mappings. In this package, that functionality is provided by ``word_to_block_dict``.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
