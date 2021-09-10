
import importlib.resources
import json

import textstada

from . import data


def load_contractions():
    with importlib.resources.open_text(data, "common_contractions.json") as file:
        return json.load(file)


def load_contraction_exceptions():
    with importlib.resources.open_text(data, "common_contractions_exceptions.txt") as file:
        return file.read().split()


def load_pronouns():
    with importlib.resources.open_text(data, "pronouns.txt") as file:
        return file.read().split()

CONTRACTIONS = load_contractions()
CONTRACTIONS_EXCEPTIONS = load_contraction_exceptions()
PRONOUNS = load_pronouns()

PUNCT_ALL = '!"#$£€%&\'()*+,-./:;<=>?@[\\]^_`{|}~©™•_”~[]¦¬'
PUNCT_BASIC = '.,?!()%&'

# Pipeline
FULLMONTY = [
    'replace_latin_abbrevs',
    'space_sentencestops',
    'clean_quote_chars',
    'replace_contractions',
    'add_fullstop',
    'remove_dashes',
    'remove_bullets',
    'remove_numerical_commas',
    'remove_punctuation',
    'space_sentencestops',
    'single_space'
]