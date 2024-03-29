import re
import warnings

import pandas as pd
from my_utils import (
    additional_stopwords,
    companies,
    federal_instances,
    industries,
    politicians,
)
from natasha import (
    Doc,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsNERTagger,
    Segmenter,
)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm.auto import tqdm

warnings.filterwarnings("ignore")

stop_words = stopwords.words("russian") + additional_stopwords

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
ner_tagger = NewsNERTagger(emb)


def prepare_text(text: str) -> str:
    """
    Remove excessive \n, spaces, and tags, brackets, digits.

    :param text: body of the text (news)
    :type text: str

    :rtype: str
    :return res_text: prepared text
    """
    del_n = re.compile("\n")
    del_tags = re.compile("<[^>]*>")
    del_brackets = re.compile("\([^)]*\)")
    clean_text = re.compile("[^а-яa-z\s]")
    del_spaces = re.compile("\s{2,}")

    text = del_n.sub(" ", str(text).lower())
    text = del_tags.sub("", text)
    text = del_brackets.sub("", text)
    text = clean_text.sub("", text)
    res_text = del_spaces.sub(" ", text)
    return res_text


def del_stopwords(text: str) -> str:
    """
    Remove stopwords.

    :param text: body of the text (news)
    :type text: str

    :rtype: str
    :return res_text: prepared text
    """
    clean_tokens = tuple(
        map(lambda x: x if x not in stop_words else "", word_tokenize(text)),
    )
    res_text = " ".join(clean_tokens)
    return res_text


def lemmatize_text(text: str) -> str:
    """
    Lemmatize text.

    :param text: body of the text (news)
    :type text: str

    :rtype: str
    :return res_text: lemmatized text
    """
    doc = Doc(text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    for token in doc.tokens:
        token.lemmatize(morph_vocab)

    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        span.normalize(morph_vocab)

    res_text = " ".join([token.lemma for token in doc.tokens])
    return res_text


def ner_and_clear_text(df: pd.DataFrame) -> None:
    """
    Complete all text cleaning steps and NER.

    :param df: dataset
    :type df: pd.DataFrame
    """

    for i in tqdm(range(df.shape[0]), desc="NER and clear texts"):
        text = df.loc[i, "body"]
        text = prepare_text(text)
        text = del_stopwords(text)

        df.loc[i, "text_clear"] = lemmatize_text(
            text=text,
        )


def filter_ne(clear_texts: str, filter_dict: dict) -> list[list[str]]:
    """
    Filter named entities found during NER step according to passed dictionary.

    :param clear_texts: cleared lemmatized text
    :type clear_texts: str
    :param filter_dict: dictionary of target named entities
    :type filter_dict: dict

    :rtype: list[list[str]]
    :return lst: list of lists of target named entities in texts
    """
    lst = []

    for clear_text in clear_texts:
        help_lst = []
        for key, pattern in filter_dict.items():
            obj = re.search(pattern, clear_text)
            if obj:
                help_lst.append(key)

        lst.append(help_lst)

    return lst


def create_column_with_ne(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create column with named entities found in the corresponding text.

    :param df: dataset
    :type df: pd.DataFrame

    :rtype: pd.DataFrame
    :return data: dataset with found NE as column
    """
    companies_lst = filter_ne(df["text_clear"], companies)
    fed_and_polit_lst = filter_ne(df["text_clear"], federal_instances | politicians)

    data = pd.DataFrame(columns=[*df.columns, "companies"])
    rows_to_insert = []

    for i in range(df.shape[0]):
        if (len(companies_lst[i]) != 0) or (len(fed_and_polit_lst[i]) != 0):
            rows_to_insert.append(
                {
                    "website": df.loc[i, "website"],
                    "section": df.loc[i, "section"],
                    "url": df.loc[i, "url"],
                    "header": df.loc[i, "header"],
                    "body": df.loc[i, "body"],
                    "key_words": df.loc[i, "key_words"],
                    "body_length": df.loc[i, "body_length"],
                    "datetime": df.loc[i, "datetime"],
                    "text_clear": df.loc[i, "text_clear"],
                    "companies": companies_lst[i],
                },
            )

    data = pd.concat([data, pd.DataFrame(rows_to_insert)], ignore_index=True)

    return data


def create_companies_dataset(
    df: pd.DataFrame,
    number_of_companies_in_one_news: int,
) -> pd.DataFrame:
    """
    Create dataset with companies as named entities.

    :param df: dataset
    :type df: pd.DataFrame
    :param number_of_companies_in_one_news: number of companies as NE that could
     be in one text
    :type number_of_companies_in_one_news: int

    :rtype: pd.DataFrame
    :return final_comp_df: dataset with companies as named entities
    """
    final_comp_df = pd.DataFrame(columns=[*df.columns]).drop(["companies"], axis=1)
    rows_to_insert = []

    comp_df = df[df["companies"].apply(lambda x: len(x) != 0)].reset_index()

    for i in range(len(comp_df)):
        if len(comp_df.loc[i, "companies"]) <= number_of_companies_in_one_news:
            for company in comp_df.loc[i, "companies"]:
                rows_to_insert.append(
                    {
                        "website": comp_df.loc[i, "website"],
                        "section": comp_df.loc[i, "section"],
                        "url": comp_df.loc[i, "url"],
                        "header": comp_df.loc[i, "header"],
                        "body": comp_df.loc[i, "body"],
                        "key_words": comp_df.loc[i, "key_words"],
                        "body_length": comp_df.loc[i, "body_length"],
                        "text_clear": comp_df.loc[i, "text_clear"],
                        "datetime": comp_df.loc[i, "datetime"],
                        "company": company,
                    },
                )

    final_comp_df = pd.concat(
        [final_comp_df, pd.DataFrame(rows_to_insert)],
        ignore_index=True,
    )

    return final_comp_df


def create_industries_dataset(
    df: pd.DataFrame,
    number_of_companies_in_one_news: int,
) -> pd.DataFrame:
    """
    Create dataset with industries as named entities.

    :param df: dataset
    :type df: pd.DataFrame
    :param number_of_companies_in_one_news: number of companies as NE that could
     be in one text
    :type number_of_companies_in_one_news: int

    :rtype: pd.DataFrame
    :return final_comp_df: dataset with industries as named entities
    """
    comp_df = df[df["companies"].apply(lambda x: len(x) != 0)].reset_index()

    ind_df = pd.DataFrame(columns=[*df.columns, "industry"]).drop(["companies"], axis=1)
    rows_to_insert = []

    for i in range(len(comp_df)):
        if len(comp_df.loc[i, "companies"]) <= number_of_companies_in_one_news:
            ind_lst = []
            for company in comp_df.loc[i, "companies"]:
                for industry, ind_companies in industries.items():
                    if company in ind_companies and industry not in ind_lst:
                        ind_lst.append(industry)

                        rows_to_insert.append(
                            {
                                "website": comp_df.loc[i, "website"],
                                "section": comp_df.loc[i, "section"],
                                "url": comp_df.loc[i, "url"],
                                "header": comp_df.loc[i, "header"],
                                "body": comp_df.loc[i, "body"],
                                "key_words": comp_df.loc[i, "key_words"],
                                "body_length": comp_df.loc[i, "body_length"],
                                "datetime": comp_df.loc[i, "datetime"],
                                "text_clear": comp_df.loc[i, "text_clear"],
                                "industry": industry,
                            },
                        )

    ind_df = pd.concat([ind_df, pd.DataFrame(rows_to_insert)], ignore_index=True)

    return ind_df


def ner_and_new_datasets(
    df: pd.DataFrame,
    number_of_companies_in_one_news: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Complete all steps to get companies, industries and global datasets.

    :param df: dataset
    :type df: pd.DataFrame
    :param number_of_companies_in_one_news: number of companies as NE that could
     be in one text
    :type number_of_companies_in_one_news: int

    :rtype: (pd.DataFrame, pd.DataFrame, pd.DataFrame)
    :return (final_comp_df, final_ind_df, final_glob_df):
    (companies dataset, industries dataset, global dataset)
    """
    ner_and_clear_text(df)
    data = create_column_with_ne(df=df)

    final_comp_df = create_companies_dataset(
        df=data,
        number_of_companies_in_one_news=number_of_companies_in_one_news,
    )
    final_ind_df = create_industries_dataset(
        df=data,
        number_of_companies_in_one_news=number_of_companies_in_one_news,
    )
    final_glob_df = data.drop(["companies"], axis=1)

    return final_comp_df, final_ind_df, final_glob_df
