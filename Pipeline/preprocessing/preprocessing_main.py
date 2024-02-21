import hydra
import pandas as pd
from __init__ import PROJECT_ROOT
from omegaconf import DictConfig
from soft_preprocessing import soft_preprocess


@hydra.main(
    config_path=str(PROJECT_ROOT / "configs" / "preprocessing"),
    config_name="basic_preprocessing_config.yaml",
    version_base="1.3",
)
def run_preprocessing(cfg: DictConfig) -> None:
    df = pd.read_parquet(f"{cfg.initial_data_path}/{cfg.initial_file}")
    soft_preprocess(df)

    print(df)


if __name__ == "__main__":
    run_preprocessing()
