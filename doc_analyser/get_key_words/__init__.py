from string import punctuation
from collections import Counter
import re

def generate_key_words(nlp_model, text):
    text = re.sub(r'\[[0-9]*\]', ' ', text).replace('(', '').replace(')', '')
    text = re.sub(r'\s+', ' ', text)

    res = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    doc = nlp_model(text.lower())

    for token in doc:
        if(token.text in nlp_model.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            res.append(token.text)

    common = Counter(res).most_common(100)

    return {
        'tagsWithFreqs': {
            x[0] : x[1] for x in common
            },
        'tagsText' :
            [x[0] for x in common]
        }