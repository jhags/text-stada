
import json
import re

from textstada import config


# Additional functions
# ====================
# punctation
# special characters
# prefixes
# remove stopwords (small med and large lists?)
# spelling corrections
# list all acronyms (utils)
# list all text between quotes e.g. "lorum ipsum"
# abbriviations such as e.g. or i.e. or N.B. --> eg, ie, NB


def vectorize(func, **args):
    def wrapper(x, **args):
        if isinstance(x, list):
            return [func(i, **args) for i in x]
        return func(x, **args)
    return wrapper


@vectorize
def single_space(text):
    """ replace multiple whitespaces with a single space. """
    rx = r"\s{2,}"
    text = re.sub(rx, " ", text)
    return text.strip()


@vectorize
def space_sentencestops(text, stop_chars=".;!?,:"):
    """ Space end of sentence punctuation marks e.g. Bad stop.Good stop. --> Bad stop. Good stop. And remove spaces before end marks e.g. Bad .Good --> Bad. Good."""
    # Add a single space after each stop character
    for c in stop_chars:
        rx = rf"(\{c}(?=[a-zA-Z]))"
        text = re.sub(rx, f"{c} ", text)

    # Remove the preceding space before a stop charater
    rx = fr"((?<=[a-zA-Z0-9])\s{{1,}}(?=[{stop_chars}]))"
    text = re.sub(rx, '', text)

    return text


@vectorize
def add_fullstop(text, stop_chars='.?!', replace_chars=';:,-/'):
    """ Add a fullstop to the end of a string if it does not exist """
    text = text.strip()
    if replace_chars is not None:
        if text[-1] in replace_chars:
            text = text[0:-1]
            return add_fullstop(text, stop_chars=stop_chars, replace_chars=replace_chars)
    if text[-1] not in stop_chars:
        text+='.'
    return text


@vectorize
def remove_numerical_commas(text):
    """ Remove commas from numerical numbers e.g. 1,000,000 --> 1000000 """
    rx = r"((?<=\d)\,(?=\d))"
    return re.sub(rx, "", text)


@vectorize
def remove_dashes(text):
    """ Remove dashes between acronym-styled words where the character preceding the dash is an upper-case letter and the character following the dash is either an upper-case letter or digit, e.g. COVID-19 --> COVID19. one-to-one --> one-to-one."""
    # Replace all long dashes with short dashes everywhere
    rx = r"\–"
    text = re.sub(rx, "-", text)

    # remove dashes between word and numbers
    rx = r"((?<=[A-Z])\-(?=[A-Z|\d]))"
    text = re.sub(rx, "", text)

    # remove dashes seperated by white spaces. incl long and short dashes
    rx = r"((?<=\s){1,}\-{1,}(?=\s){1,})"
    text = re.sub(rx, "", text)

    # Remove dashes at the start of a string
    rx = r"(^\-(?=\s){1,})"
    text = re.sub(rx, "", text)
    return text


@vectorize
def remove_bullets(text):
    """ Remove bullet characters and replace with fullstop. """
    # Remove bullets at start of string and replace with space
    text = text.strip()
    rx = r"^\•"
    text = re.sub(rx, ' ', text)

    # remove any other bullet and replace with fullstop
    rx = r"\•"
    text = re.sub(rx, '.', text)
    text = text.strip()
    return space_sentencestops(text)


def replace_acronyms(text, acronyms):
    for k, v in acronyms.items():
        for i in v:
            rx = rf"\b({i})\b"
            text = re.sub(rx, k, text, flags=re.IGNORECASE)

    return ' '.join(text.split())


@vectorize
def remove_escapes(text):
    """ Remove escape characters and replace with fullstop except if the escape is at the start of a string. """
    escapes = [r'\n', r'\t', r'\r']
    text = text.strip()
    for escape in escapes:
        rx = fr"^\{escape}"
        text = re.sub(rx, ' ', text)

    for escape in escapes:
        rx = fr"\{escape}"
        text = re.sub(rx, '.', text)

    text = text.strip()
    return space_sentencestops(text)


@vectorize
def replace_contractions(text):
    """ Replace common contractions (e.g. don't) with full form (e.g. do not). The list of contractions have been derived from wikipedia (see: List of English contractions)."""
    for k, v in config.CONTRACTIONS.items():
        # sub exact matches
        rx = rf"((?<=\s)|^)({k})((?=\s)|$)"
        text = re.sub(rx, v, text, flags=re.IGNORECASE)

        # sub words that missed the apostraphy
        k = k.replace("'", "")
        rx = rf"((?<=\s)|^)({k})((?=\s)|$)"
        text = re.sub(rx, v, text, flags=re.IGNORECASE)

    return text


@vectorize
def clean_quote_chars(text):
    """ Simply usage of quotations and single apostraphies including (‘ ’ ´) and (“ ”) """
    rx = r"[‘’´]"
    text = re.sub(rx, "'", text)

    rx = r"[“”]"
    text = re.sub(rx, '"', text)
    return text


@vectorize
def replace_latin_abbrevs(text):
    """ Replace Latin abbreviations (eg, ie, and NB) with tidier forms (such as: (e.g.|e. g.|e.g) --> eg)"""
    abr = [r"e\.g\.", r"e\. g\.", r"e\.g"]
    for i in abr:
        rx = fr"((?<=\s)|^)({i})((?=\s)|$)"
        text = re.sub(rx, "eg", text, flags=re.IGNORECASE)

    abr = [r"i\.e\.", r"i\. e\.", r"i\.e"]
    for i in abr:
        rx = fr"((?<=\s)|^)({i})((?=\s)|$)"
        text = re.sub(rx, "ie", text, flags=re.IGNORECASE)

    abr = [r"n\.b\.", r"n\. b\.", r"n\.b"]
    for i in abr:
        rx = fr"((?<=\s)|^)({i})((?=\s)|$)"
        text = re.sub(rx, "nb", text, flags=re.IGNORECASE)
    return text


@vectorize
def remove_pronouns(text):
    """ Remove pronouns from text """
    text = replace_contractions(text)

    for pronoun in config.PRONOUNS:
        rx = rf"\b({pronoun})\b"
        text = re.sub(rx, '', text, flags=re.IGNORECASE)

    return single_space(text)