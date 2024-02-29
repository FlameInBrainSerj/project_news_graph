import os

import hydra
import pandas as pd
from __init__ import PROJECT_ROOT
from ner_and_clean_texts import ner_and_new_datasets
from omegaconf import DictConfig
from sklearn.model_selection import train_test_split
from soft_preprocessing import soft_preprocess
from trade_data_injection import inject_trade_data


@hydra.main(
    config_path=str(PROJECT_ROOT / "configs" / "preprocessing"),
    config_name="basic_preprocessing_config.yaml",
    version_base="1.3",
)
def run_preprocessing_and_save_data(
    cfg: DictConfig,
) -> None:
    """
    Run all preprocessing of the data and save the data with split on train and test.

    :param cfg: configs
    :type cfg: DictConfig
    """
    # Create folders for preprocessed data
    os.system(f"mkdir {str(PROJECT_ROOT / cfg.final_data_train_path)}")
    os.system(f"mkdir {str(PROJECT_ROOT / cfg.final_data_val_path)}")
    os.system(f"mkdir {str(PROJECT_ROOT / cfg.final_data_test_path)}")

    df = pd.read_parquet(f"{cfg.initial_data_path}/{cfg.initial_file}")
    soft_preprocess(df)
    comp_df, ind_df, glob_df = ner_and_new_datasets(
        df=df,
        number_of_companies_in_one_news=int(cfg.number_of_companies_in_one_news),
    )
    inject_trade_data(comp_df=comp_df, ind_df=ind_df, glob_df=glob_df)

    # Split company data on train/val/test
    comp_df_train, comp_df_test = train_test_split(
        comp_df,
        test_size=cfg.proportion_split,
    )
    comp_df_train, comp_df_val = train_test_split(
        comp_df_train,
        test_size=cfg.proportion_split,
    )

    # Split industry data on train/val/test
    ind_df_train, ind_df_test = train_test_split(
        ind_df,
        test_size=cfg.proportion_split,
    )
    ind_df_train, ind_df_val = train_test_split(
        ind_df_train,
        test_size=cfg.proportion_split,
    )

    # Split global data on train/val/test
    glob_df_train, glob_df_test = train_test_split(
        glob_df,
        test_size=cfg.proportion_split,
    )
    glob_df_train, glob_df_val = train_test_split(
        glob_df_train,
        test_size=cfg.proportion_split,
    )

    # Split train/val/test company data
    comp_df_train.to_parquet(
        f"{cfg.final_data_train_path}/comp_data.parquet",
        index=False,
    )
    comp_df_val.to_parquet(
        f"{cfg.final_data_val_path}/comp_data.parquet",
        index=False,
    )
    comp_df_test.to_parquet(
        f"{cfg.final_data_test_path}/comp_data.parquet",
        index=False,
    )

    # Split train/val/test industry data
    ind_df_train.to_parquet(
        f"{cfg.final_data_train_path}/ind_data.parquet",
        index=False,
    )
    ind_df_val.to_parquet(
        f"{cfg.final_data_val_path}/ind_data.parquet",
        index=False,
    )
    ind_df_test.to_parquet(
        f"{cfg.final_data_test_path}/ind_data.parquet",
        index=False,
    )

    # Split train/val/test global data
    glob_df_train.to_parquet(
        f"{cfg.final_data_train_path}/glob_data.parquet",
        index=False,
    )
    glob_df_val.to_parquet(
        f"{cfg.final_data_val_path}/glob_data.parquet",
        index=False,
    )
    glob_df_test.to_parquet(
        f"{cfg.final_data_test_path}/glob_data.parquet",
        index=False,
    )


if __name__ == "__main__":
    run_preprocessing_and_save_data()
