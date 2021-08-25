
import json
import importlib.resources
from . import data

def load_contractions():
    with importlib.resources.open_text(data, "common_contractions.json") as file:
        return json.load(file)

CONTRACTIONS = load_contractions()
