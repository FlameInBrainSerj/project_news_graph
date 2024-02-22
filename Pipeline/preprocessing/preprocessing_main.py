import hydra
import pandas as pd
from __init__ import PROJECT_ROOT
from ner_and_clean_texts import ner_and_new_datasets
from omegaconf import DictConfig
from soft_preprocessing import soft_preprocess


@hydra.main(
    config_path=str(PROJECT_ROOT / "configs" / "preprocessing"),
    config_name="basic_preprocessing_config.yaml",
    version_base="1.3",
)
def run_preprocessing(cfg: DictConfig) -> None:
    """
    Run all preprocessing of the data.

    :param cfg: configs
    :type cfg: DictConfig
    """
    df = pd.read_parquet(f"{cfg.initial_data_path}/{cfg.initial_file}")
    soft_preprocess(df)
    comp_df, ind_df, final_glob_df = ner_and_new_datasets(
        df=df,
        number_of_companies_in_one_news=int(cfg.number_of_companies_in_one_news),
    )

    print(final_glob_df)


if __name__ == "__main__":
    run_preprocessing()
