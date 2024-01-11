import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsNERTagger,
    Doc,
)

from utils.verification_dict import companies, additional_stopwords

nltk.download("stopwords")
nltk.download("punkt")

del_n = re.compile("\n")
del_tags = re.compile("<[^>]*>")
del_brackets = re.compile("\([^)]*\)")
del_spaces = re.compile("\s{2,}")
clean_text = re.compile("[^а-яa-z\s]")
stop_words = stopwords.words("russian") + additional_stopwords


def initialize_natasha():
    """
    Initialize natasha for NER.
    """
    global segmenter, morph_vocab, emb, morph_tagger, ner_tagger

    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    ner_tagger = NewsNERTagger(emb)


def clear_text(text: str):
    """
    Clear text from mess.

    :param text: text which will be cleared
    :type text: str

    :rtype: str
    :return text: cleared text
    """
    text = del_n.sub(" ", str(text).lower())
    text = del_tags.sub("", text)
    text = del_brackets.sub("", text)
    res_text = clean_text.sub("", text)
    return del_spaces.sub(" ", res_text)


def del_stopwords(text: str):
    """
    Delete stopwords.

    :param text: text where stopwords will be deleted
    :type text: str

    :rtype: str
    :return text: text without stopwords
    """
    clean_tokens = tuple(
        map(lambda x: x if x not in stop_words else "", word_tokenize(text))
    )
    res_text = " ".join(clean_tokens)
    return res_text


def lemmatize(text: str):
    """
    Lemmatize the text.

    :param text: text which will be lemmatized
    :type text: str

    :rtype: str
    :return text: lemmatized text
    """
    text = Doc(text)
    text.segment(segmenter)
    text.tag_morph(morph_tagger)
    for token in text.tokens:
        token.lemmatize(morph_vocab)
    text.tag_ner(ner_tagger)
    for span in text.spans:
        span.normalize(morph_vocab)
    return " ".join([token.lemma for token in text.tokens])


def ner_and_clear_text(text: str):
    """
    Get the cleared lemmatized text without stopword and get its level.

    :param text: raw text of the news
    :type text: str

    :rtype: int
    :return level: level
    :rtype: str
    :return text: lemmatized text
    """
    text = clear_text(text)
    text = del_stopwords(text)
    text = lemmatize(text)

    for key, pattern in companies.items():
        obj = re.search(pattern, text)
        if obj:
            return 3, text

    return 1, text
