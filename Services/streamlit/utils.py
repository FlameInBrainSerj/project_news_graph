from datetime import datetime

import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots
from scipy.sparse.linalg import eigsh
from sklearn.cluster import KMeans

import streamlit as st

months = {
    "января": "1",
    "февраля": "2",
    "марта": "3",
    "апреля": "4",
    "мая": "5",
    "июня": "6",
    "июля": "7",
    "августа": "8",
    "сентября": "9",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
}


@st.cache_data
def plot_news(source: str, news_by_date: list) -> go.Figure:
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=news_by_date.index,
            y=weekend,
            fill="tonexty",
            fillcolor="rgba(255, 0, 0, 0.4)",
            line_shape="hv",
            line_color="rgba(0,0,0,0)",
            showlegend=True,
            name="Weekends and holidays",
        ),
        row=1,
        col=1,
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(
            x=list(news_by_date.index),
            y=list(news_by_date.values),
            line_color="rgba(65,105,225,1)",
            name="News per day",
        )
    )

    fig.update_layout(
        title="News per day {}".format(source),
        width=1200,
        height=450,
        xaxis=dict(rangeselector=dict(),
                   rangeslider=dict(visible=True),
                   type="date"),
    )
    return fig


@st.cache_data
def create_date_series():
    years = [
        "2019-01-01",
        "2020-01-01",
        "2021-01-01",
        "2022-01-01",
        "2023-01-01",
        "2024-01-01",
    ]
    working_days = []
    for i in range(len(years) - 1):
        start = years[i]
        finish = years[i + 1]
        candles = requests.get(
            "http://iss.moex.com/iss/engines/stock/markets/shares/securities/"
            "sber/candles.json?from={}&till={}&interval=24".format(start,
                                                                   finish)
        ).json()
        for day in range(len(candles["candles"]["data"])):
            working_days.append(
                datetime.strptime(
                    candles["candles"]["data"][day][6], "%Y-%m-%d %H:%M:%S"
                )
            )
    weekend = pd.Series()
    s = pd.date_range("2019-01-01", "2024-01-01", freq="D").to_series()
    for i in s:
        if i not in working_days:
            weekend[i] = 1
        else:
            weekend[i] = 0
    return s, weekend, working_days


s, weekend, working_days = create_date_series()


def create_news_by_date(df: pd.DataFrame):
    dates = []
    for i in df.index:
        dates.append(datetime.date(df["datetime"][i]))
    df["date"] = dates
    news_by_date = df.groupby("date").date.count()
    news_by_date = news_by_date.reindex(s, fill_value=0)
    return news_by_date


@st.cache_data
def create_filtered_dataframe(df: pd):
    ts_total = df.copy()
    ts_total.index = ts_total["datetime"]
    ts_total = ts_total[
        ts_total.index.weekday < 5].between_time("9:30", "23:30")
    ts_total = ts_total[
        ts_total["date"].isin(pd.Series(working_days).dt.date.tolist())]
    ts_total = ts_total.sort_index().loc["2019-01-01":"2024-01-01", :]
    return ts_total


def spectral_clusterization(G, k=9):
    A = nx.adjacency_matrix(G).todense()
    D = np.diag(np.sum(A, axis=1))
    L = D - A
    D_inv_sqrt = np.linalg.inv(np.sqrt(D))
    L_norm = D_inv_sqrt @ L @ D_inv_sqrt
    eigvals, eigvecs = eigsh(L_norm, k=k, which="SM")
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(eigvecs)
    labels = kmeans.labels_
    res = {list(G.nodes)[i]: labels[i] for i in range(len(list(G.nodes)))}
    return res


node_classes = {
    # Нефть и газ
    "MOEXOG": ["BANE",
               "GAZP",
               "LKOH",
               "NVTK",
               "RNFT",
               "ROSN",
               "SNGS",
               "TATN",
               "TRNF"],
    # Электроэнергетики
    "MOEXEU": [
        "IRAO",
        "HYDR",
        "FEES",
        "MSNG",
        "UPRO",
        "LSNG",
        "RSTI",
        "OGKB",
        "MRKP",
        "MRKC",
        "ELFV",
        "TGKA",
        "MSRS",
        "MRKU",
        "TGKB",
        "DVEC",
        "MRKZ",
        "MRKV",
    ],
    # Телекоммуникации
    "MOEXTL": ["MTSS",
               "RTKM",
               "MGTS",
               "TTLK"],
    # Металлы и добыча
    "MOEXMM": [
        "GMKN",
        "PLZL",
        "CHMF",
        "NLMK",
        "POLY",
        "ALRS",
        "MAGN",
        "RUAL",
        "ENPG",
        "MTLR",
        "VSMO",
        "SELG",
        "RASP",
        "SGZH",
        "CHMK",
    ],
    # Финансы
    "MOEXFN": ["SBER",
               "TCSG",
               "VTBR",
               "CBOM",
               "BSPB",
               "QIWI",
               "RENI",
               "SFIN",
               "AFKS"],
    # Потребительский сектор
    "MOEXCN": [
        "MGNT",
        "FIVE",
        "FIXP",
        "AGRO",
        "GEMC",
        "LENT",
        "BELU",
        "MDMG",
        "AQUA",
        "MVID",
        "APTK",
        "SVAV",
        "WUSH",
        "ABIO",
        "OKEY",
    ],
    # Химия и нефтехимия
    "MOEXCH": ["PHOR",
               "KAZT",
               "AKRN",
               "NKNC",
               "KZOS"],
    # Транспорт
    "MOEXTN": ["GLTR",
               "FLOT",
               "AFLT",
               "NMTP",
               "FESH",
               "NKHP",
               "RKKE"],
    # Информационные технологии
    "MOEXIT": ["CIAN",
               "HHRU",
               "OZON", "POSI",
               "VKCO",
               "YNDX"],
    # Строительные компании
    "MOEXRE": ["ETLN",
               "LSRG",
               "PIKK",
               "SMLT"],
}


node_classes_new = {}
for keys, values in node_classes.items():
    for i in values:
        node_classes_new[i] = keys
