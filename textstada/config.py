
import json
import importlib.resources
from . import data

def load_contractions():
    with importlib.resources.open_text(data, "common_contractions.json") as file:
        return json.load(file)

def load_pronouns():
    with importlib.resources.open_text(data, "pronouns.txt") as file:
        return file.read().split()

CONTRACTIONS = load_contractions()
PRONOUNS = load_pronouns()

PUNCT_ALL = '!"#$£€%&\'()*+,-./:;<=>?@[\\]^_`{|}~©™•_”~[]¦¬'
PUNCT_BASIC = '.?!()%&'
