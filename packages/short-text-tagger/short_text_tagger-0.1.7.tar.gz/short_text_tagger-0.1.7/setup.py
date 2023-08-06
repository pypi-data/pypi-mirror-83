#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["pandas>=0.24.0","nltk>=3.5"]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="John Anthony Bowllan",
    author_email='jbowllan@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Short-text tagger generates topic distributions for all texts in a corpus.",
    entry_points={
        'console_scripts': [
            'short_text_tagger=short_text_tagger.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='short_text_tagger',
    name='short_text_tagger',
    packages=find_packages(include=['short_text_tagger', 'short_text_tagger.short_text_tagger']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/JohnAnthonyBowllan/short_text_tagger',
    version='0.1.7',
    zip_safe=False,
)
