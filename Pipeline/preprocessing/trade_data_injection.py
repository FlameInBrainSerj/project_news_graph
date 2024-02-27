import time
from datetime import timedelta

import numpy as np
import pandas as pd
import requests
from my_utils import third_thursday
from tqdm.auto import tqdm

CONNECT_TIMEOUT = 300
READ_TIMEOUT = 300


def inject_comp_data(comp_df: pd.DataFrame) -> None:
    """
    Inject companies' NE data.

    :param comp_df: dataset
    :type comp_df: pd.DataFrame
    """
    companies_string = (
        "http://iss.moex.com/iss/engines/stock/markets/shares"
        "/securities/{}/candles.json?from={}&till={}&interval=1"
    )

    comp_df["price_release"] = np.nan
    comp_df["price_lag_30"] = np.nan
    comp_df.sort_values(by=["datetime"], inplace=True)

    for i in tqdm(range(len(comp_df)), desc="Inject companies' NE data"):
        start = comp_df["datetime"][i]
        end = comp_df["datetime"][i] + timedelta(minutes=30)
        company = comp_df["company"][i]

        data = requests.get(
            companies_string.format(company, start, end),
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
        ).json()

        try:
            comp_df.loc[i, "price_release"] = data["candles"]["data"][0][0]
            comp_df.loc[i, "price_lag_30"] = data["candles"]["data"][-1][0]
        except IndexError:
            continue

    comp_df.dropna(subset=["price_release", "price_lag_30"], inplace=True)
    comp_df.reset_index(drop=True, inplace=True)

    comp_df["price_diff"] = comp_df["price_lag_30"] - comp_df["price_release"]
    comp_df["price_diff_percent"] = (
        comp_df["price_diff"] / comp_df["price_release"] * 100
    )


def inject_ind_data(ind_df: pd.DataFrame) -> None:
    """
    Inject industries' NE data.

    :param ind_df: dataset
    :type ind_df: pd.DataFrame
    """
    ind_string = (
        "http://iss.moex.com/iss/engines/stock/markets/index/boards"
        "/SNDX/securities/{}/candles.json?from={}&till={}&interval=1"
    )

    ind_df["price_release"] = np.nan
    ind_df["price_lag_30"] = np.nan
    ind_df.sort_values(by=["datetime"], inplace=True)

    for i in tqdm(range(len(ind_df)), desc="Inject industries' NE data"):
        start = ind_df["datetime"][i]
        end = ind_df["datetime"][i] + timedelta(minutes=30)
        ind = ind_df["industry"][i]

        data = requests.get(
            ind_string.format(ind, start, end),
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
        ).json()

        try:
            ind_df.loc[i, "price_release"] = data["candles"]["data"][0][0]
            ind_df.loc[i, "price_lag_30"] = data["candles"]["data"][-1][0]
        except IndexError:
            continue

    ind_df.dropna(subset=["price_release", "price_lag_30"], inplace=True)
    ind_df.reset_index(drop=True, inplace=True)

    ind_df["price_diff"] = ind_df["price_lag_30"] - ind_df["price_release"]
    ind_df["price_diff_percent"] = ind_df["price_diff"] / ind_df["price_release"] * 100


def inject_glob_data(glob_df: pd.DataFrame) -> None:
    """
    Inject global' NE data.

    :param glob_df: dataset
    :type glob_df: pd.DataFrame
    """
    global_moex = (
        "http://iss.moex.com/iss/engines/stock/markets/index/boards"
        "/SNDX/securities/{}/candles.json?from={}&till={}&interval=1"
    )
    global_rvi = (
        "http://iss.moex.com/iss/engines/stock/markets/index/boards"
        "/RTSI/securities/RVI/candles.json?from={}&till={}&interval=1"
    )
    global_usd_rub_fut = (
        "http://iss.moex.com/iss/engines/futures/markets/forts/boards"
        "/RFUD/securities/{}/candles.json?from={}&till={}&interval=1"
    )

    glob_df["imoex_price_release"] = np.nan
    glob_df["imoex_price_lag_30"] = np.nan
    glob_df["rvi_price_release"] = np.nan
    glob_df["rvi_price_lag_30"] = np.nan
    glob_df["usd_price_release"] = np.nan
    glob_df["usd_price_lag_30"] = np.nan
    glob_df.sort_values(by=["datetime"], inplace=True)

    for i in tqdm(range(len(glob_df)), desc="Inject global' NE data"):
        time.sleep(0.1)

        start = glob_df["datetime"][i]
        end = glob_df["datetime"][i] + timedelta(minutes=30)

        # Get IMOEX data
        if str(start.time()) < "18:35:00":
            data_imoex_1 = requests.get(
                global_moex.format("IMOEX", start, end),
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            ).json()
            try:
                glob_df.loc[i, "imoex_price_release"] = data_imoex_1["candles"]["data"][
                    0
                ][0]
                glob_df.loc[i, "imoex_price_lag_30"] = data_imoex_1["candles"]["data"][
                    -1
                ][0]
            except IndexError:
                glob_df.loc[i, "imoex_price_release"] = np.nan
                glob_df.loc[i, "imoex_price_lag_30"] = np.nan

        elif str(start.time()) < "18:50:00":
            data_imoex_1 = requests.get(
                global_moex.format("IMOEX", start, start + timedelta(minutes=1)),
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            ).json()
            data_imoex_2 = requests.get(
                global_moex.format("IMOEX2", end, end + timedelta(minutes=1)),
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            ).json()
            try:
                glob_df.loc[i, "imoex_price_release"] = data_imoex_1["candles"]["data"][
                    0
                ][0]
                glob_df.loc[i, "imoex_price_lag_30"] = data_imoex_2["candles"]["data"][
                    0
                ][0]
            except IndexError:
                glob_df.loc[i, "imoex_price_release"] = np.nan
                glob_df.loc[i, "imoex_price_lag_30"] = np.nan

        else:
            data_imoex_2 = requests.get(
                global_moex.format("IMOEX2", start, end),
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            ).json()
            try:
                glob_df.loc[i, "imoex_price_release"] = data_imoex_2["candles"]["data"][
                    0
                ][0]
                glob_df.loc[i, "imoex_price_lag_30"] = data_imoex_2["candles"]["data"][
                    -1
                ][0]
            except IndexError:
                glob_df.loc[i, "imoex_price_release"] = np.nan
                glob_df.loc[i, "imoex_price_lag_30"] = np.nan

        # Get RVI data
        data_rvi = requests.get(
            global_rvi.format(start, end),
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
        ).json()
        try:
            glob_df.loc[i, "rvi_price_release"] = data_rvi["candles"]["data"][0][0]
            glob_df.loc[i, "rvi_price_lag_30"] = data_rvi["candles"]["data"][-1][0]
        except IndexError:
            glob_df.loc[i, "rvi_price_release"] = np.nan
            glob_df.loc[i, "rvi_price_lag_30"] = np.nan

        # Get RUBUSD data
        year = start.year

        if str(start) < f"{year}-03-{third_thursday(year, 3)}":
            data_rubusd = requests.get(
                global_usd_rub_fut.format(f"SiH{year % 10}", start, end),
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            ).json()
            try:
                glob_df.loc[i, "usd_price_release"] = data_rubusd["candles"]["data"][0][
                    0
                ]
                glob_df.loc[i, "usd_price_lag_30"] = data_rubusd["candles"]["data"][-1][
                    0
                ]
            except IndexError:
                glob_df.loc[i, "usd_price_release"] = np.nan
                glob_df.loc[i, "usd_price_lag_30"] = np.nan

        elif str(start) < f"{year}-06-{third_thursday(year, 3)}":
            data_rubusd = requests.get(
                global_usd_rub_fut.format(f"SiM{year % 10}", start, end),
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            ).json()
            try:
                glob_df.loc[i, "usd_price_release"] = data_rubusd["candles"]["data"][0][
                    0
                ]
                glob_df.loc[i, "usd_price_lag_30"] = data_rubusd["candles"]["data"][-1][
                    0
                ]
            except IndexError:
                glob_df.loc[i, "usd_price_release"] = np.nan
                glob_df.loc[i, "usd_price_lag_30"] = np.nan

        elif str(start) < f"{year}-09-{third_thursday(year, 3)}":
            data_rubusd = requests.get(
                global_usd_rub_fut.format(f"SiU{year % 10}", start, end),
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            ).json()
            try:
                glob_df.loc[i, "usd_price_release"] = data_rubusd["candles"]["data"][0][
                    0
                ]
                glob_df.loc[i, "usd_price_lag_30"] = data_rubusd["candles"]["data"][-1][
                    0
                ]
            except IndexError:
                glob_df.loc[i, "usd_price_release"] = np.nan
                glob_df.loc[i, "usd_price_lag_30"] = np.nan

        elif str(start) < f"{year}-12-{third_thursday(year, 3)}":
            data_rubusd = requests.get(
                global_usd_rub_fut.format(f"SiZ{year % 10}", start, end),
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            ).json()
            try:
                glob_df.loc[i, "usd_price_release"] = data_rubusd["candles"]["data"][0][
                    0
                ]
                glob_df.loc[i, "usd_price_lag_30"] = data_rubusd["candles"]["data"][-1][
                    0
                ]
            except IndexError:
                glob_df.loc[i, "usd_price_release"] = np.nan
                glob_df.loc[i, "usd_price_lag_30"] = np.nan

        else:
            data_rubusd = requests.get(
                global_usd_rub_fut.format(f"SiH{((year + 1) % 10)}", start, end),
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            ).json()
            try:
                glob_df.loc[i, "usd_price_release"] = data_rubusd["candles"]["data"][0][
                    0
                ]
                glob_df.loc[i, "usd_price_lag_30"] = data_rubusd["candles"]["data"][-1][
                    0
                ]
            except IndexError:
                glob_df.loc[i, "usd_price_release"] = np.nan
                glob_df.loc[i, "usd_price_lag_30"] = np.nan

    glob_df.dropna(
        subset=[
            "imoex_price_release",
            "imoex_price_lag_30",
            "rvi_price_release",
            "rvi_price_lag_30",
            "usd_price_release",
            "usd_price_lag_30",
        ],
        inplace=True,
    )
    glob_df.reset_index(drop=True, inplace=True)

    glob_df["imoex_price_diff"] = (
        glob_df["imoex_price_lag_30"] - glob_df["imoex_price_release"]
    )
    glob_df["imoex_price_diff_percent"] = (
        glob_df["imoex_price_diff"] / glob_df["imoex_price_release"] * 100
    )
    glob_df["rvi_price_diff"] = (
        glob_df["rvi_price_lag_30"] - glob_df["rvi_price_release"]
    )
    glob_df["rvi_price_diff_percent"] = (
        glob_df["rvi_price_diff"] / glob_df["rvi_price_release"] * 100
    )
    glob_df["usd_price_diff"] = (
        glob_df["usd_price_lag_30"] - glob_df["usd_price_release"]
    )
    glob_df["usd_price_diff_percent"] = (
        glob_df["usd_price_diff"] / glob_df["usd_price_release"] * 100
    )


def inject_trade_data(
    comp_df: pd.DataFrame,
    ind_df: pd.DataFrame,
    glob_df: pd.DataFrame,
) -> None:
    """
    Inject trade data.

    :param comp_df: companies dataset
    :type comp_df: pd.DataFrame
    :param ind_df: industries dataset
    :type ind_df: pd.DataFrame
    :param glob_df: global dataset
    :type glob_df: pd.DataFrame
    """
    inject_comp_data(comp_df)
    inject_ind_data(ind_df)
    inject_glob_data(glob_df)
