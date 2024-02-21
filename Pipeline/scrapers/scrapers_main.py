from datetime import datetime, timedelta

import hydra
import pandas as pd
from __init__ import PROJECT_ROOT
from interfax_scraper import interfax_parse
from kommersant_scraper import kommersant_parse
from omegaconf import DictConfig
from ria_scraper import ria_parse
from selenium_options import options_init
from smart_lab_scraper import smart_lab_parse


@hydra.main(
    config_path=str(PROJECT_ROOT / "configs" / "scrapers"),
    config_name="basic_scrapers_config.yaml",
    version_base="1.3",
)
def run_scrapers(cfg: DictConfig) -> None:
    """
    Run all scrapers to collect data.

    :param cfg: configs
    :type cfg: DictConfig
    """
    # Get list of dates
    date_start = datetime.strptime(cfg.date_start, "%Y-%m-%d")
    date_end = datetime.strptime(cfg.date_end, "%Y-%m-%d")
    number_of_days = (abs(date_start - date_end)).days + 1

    # Lists of dates
    lst_dates_smart_lab = [
        (date_start + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(number_of_days)
    ]
    lst_dates_kommersant = [
        (date_start + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(number_of_days)
    ]
    lst_dates_interfax = [
        (date_start + timedelta(days=i)).strftime("%Y/%m/%d")
        for i in range(number_of_days)
    ]
    lst_dates_ria = [
        (date_start + timedelta(days=i)).strftime("%Y%m%d")
        for i in range(number_of_days)
    ]

    # Options for selenium webdriver
    options = options_init()

    smart_lab_parse(
        options=options,
        lst_dates=lst_dates_smart_lab,
        data_dir_path=cfg.data_path,
        start_date=cfg.date_start,
        end_date=cfg.date_end,
    )
    kommersant_parse(
        options=options,
        lst_dates=lst_dates_kommersant,
        data_dir_path=cfg.data_path,
        start_date=cfg.date_start,
        end_date=cfg.date_end,
    )
    interfax_parse(
        options=options,
        lst_dates=lst_dates_interfax,
        data_dir_path=cfg.data_path,
        start_date=cfg.date_start,
        end_date=cfg.date_end,
    )
    ria_parse(
        options=options,
        lst_dates=lst_dates_ria,
        data_dir_path=cfg.data_path,
        start_date=cfg.date_start,
        end_date=cfg.date_end,
    )


@hydra.main(
    config_path=str(PROJECT_ROOT / "configs" / "scrapers"),
    config_name="basic_scrapers_config.yaml",
    version_base="1.3",
)
def unite_data(cfg: DictConfig) -> None:
    """
    Unite 4 datasets of scraped data into one dataset.

    :param cfg: configs
    :type cfg: DictConfig
    """
    df_smart_lab = pd.read_parquet(
        f"{cfg.data_path}/smart_lab_{cfg.date_start}_{cfg.date_end}.parquet",
    )
    df_kommersant = pd.read_parquet(
        f"{cfg.data_path}/kommersant_{cfg.date_start}_{cfg.date_end}.parquet",
    )
    df_interfax = pd.read_parquet(
        f"{cfg.data_path}/interfax_{cfg.date_start}_{cfg.date_end}.parquet",
    )
    df_ria = pd.read_parquet(
        f"{cfg.data_path}/ria_{cfg.date_start}_{cfg.date_end}.parquet",
    )

    df = pd.concat(
        [df_interfax, df_smart_lab, df_ria, df_kommersant],
        axis=0,
        ignore_index=True,
    )

    df.to_parquet(
        f"{cfg.data_path}/full_data_{cfg.date_start}_{cfg.date_end}.parquet",
        index=False,
    )


if __name__ == "__main__":
    run_scrapers()
    unite_data()
