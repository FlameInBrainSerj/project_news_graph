from pathlib import Path
from typing import Any, Generator

import pandas as pd
import pytorch_lightning as pl
import torch
from omegaconf import DictConfig
from torch.utils.data import DataLoader, Dataset, random_split
from torchtext.vocab import Vocab, build_vocab_from_iterator


class NewsDataset(Dataset):
    """
    Dataset for the News data.
    """

    def __init__(
        self,
        root_dir: Path,
        main_col: str,
        class_col: str,
        target_quantile: int,
    ):
        self.root_dir = root_dir
        self.main_col = main_col
        self.class_col = class_col
        self.target_quantile = target_quantile
        self.dataset = pd.read_parquet(self.root_dir)

        # Define the classes for the dataset
        self.define_classes()

        # Define data which will be passed to DataLoader
        self.data_to_loader = self.create_dataset()

    def __len__(self) -> int:
        return self.dataset.shape[0]

    def __getitem__(self, idx: int) -> pd.DataFrame:
        return self.dataset.loc[idx, :]

    def define_classes(self) -> None:
        """
        Define classes for classification tasks.
        """

        q_l = self.dataset[self.main_col].quantile(self.target_quantile)
        q_u = self.dataset[self.main_col].quantile(1 - self.target_quantile)

        self.dataset[self.class_col] = 1
        self.dataset.loc[self.dataset[self.main_col] <= q_l, self.class_col] = 0
        self.dataset.loc[self.dataset[self.main_col] >= q_u, self.class_col] = 2

    def create_dataset(self) -> list[tuple[int, str]]:
        """
        Create dataset that will be passed to dataloader in correct format.

        :rtype: list[tuple[int, str]]
        :return data: list of tuples in format of (targe_label, text)
        """

        data = []
        for i in range(len(self.dataset)):
            data.append(
                (
                    self.dataset[self.class_col].values[i],
                    self.dataset["text_clear"].values[i],
                ),
            )
        return data


class DataModuleNews(pl.LightningDataModule):
    """
    PyTorch Lightning DataModule for handling data loading and processing.
    """

    def __init__(self, cfg: DictConfig, infer: bool = False):
        super().__init__()
        self.infer = infer

        self.train_path = cfg.data_train_path
        self.val_path = cfg.data_val_path
        self.test_path = cfg.data_test_path
        self.file_name = cfg.data_file
        self.main_col = cfg.main_col
        self.class_col = cfg.class_col
        self.target_quantile = cfg.target_quantile

        self.batch_size = cfg.batch_size
        self.dataloader_num_workers = cfg.dataloader_num_workers

        self.train_dataset: NewsDataset = None
        self.val_dataset: NewsDataset = None
        self.predict_dataset: NewsDataset = None

        self.vocab_save_path = Path(cfg.vocab_path) / cfg.vocab_file
        self.max_len = cfg.max_len
        self.min_freq = cfg.min_freq
        self.vocab: Vocab = None

    def setup(self, stage: str = None) -> None:
        """
        Set up the training, validation, and prediction datasets.
        """

        self.train_dataset = NewsDataset(
            root_dir=Path(self.train_path) / self.file_name,
            main_col=self.main_col,
            class_col=self.class_col,
            target_quantile=self.target_quantile,
        )

        self.val_dataset = NewsDataset(
            root_dir=Path(self.val_path) / self.file_name,
            main_col=self.main_col,
            class_col=self.class_col,
            target_quantile=self.target_quantile,
        )

        self.predict_dataset = NewsDataset(
            root_dir=Path(self.test_path) / self.file_name,
            main_col=self.main_col,
            class_col=self.class_col,
            target_quantile=self.target_quantile,
        )

        # Crate vocab for texts and save for it for model
        self.create_and_save_vocab()

    @staticmethod
    def tokenizer(text: str) -> list[str]:
        """
        Tokenize the text.

        :param text: text of the news
        :type text: str

        :rtype: list[str]
        :return tokenized_text: list of text's tokens
        """

        tokenized_text = text.split(" ")
        return tokenized_text

    @staticmethod
    def build_vocabulary(datasets: list[list[tuple[int, str]]]) -> Generator:
        """
        Build vocabulary from the texts.

        :param datasets: list of lists of tuple in format of (targe_label, text)
        :type datasets: list[list[tuple[int, str]]]

        :rtype: Generator
        :return DataModuleNews.tokenizer(text): generator of the tokenized texts
        """

        for dataset in datasets:
            for _, text in dataset:
                yield DataModuleNews.tokenizer(text)

    def create_and_save_vocab(self) -> None:
        """
        Create and save vocab.
        """

        self.vocab = build_vocab_from_iterator(
            DataModuleNews.build_vocabulary(
                datasets=[
                    self.train_dataset.data_to_loader,
                    self.val_dataset.data_to_loader,
                    self.predict_dataset.data_to_loader,
                ],
            ),
            min_freq=self.min_freq,
            specials=["<UNK>"],
        )

        self.vocab.set_default_index(self.vocab["<UNK>"])

        # In inference mode vocab is not saved
        if not self.infer:
            # Save vocab
            torch.save(self.vocab, self.vocab_save_path)

    def vectorize_batch(self, batch: Any) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Vectorize batches in the DataLoader.

        :param batch: DataLoader's batch
        :type batch: Any

        :rtype: tuple[torch.Tensor, torch.Tensor]
        :return (x, y): x as torch.Tensor and y as torch.Tensor
        """
        y, x = list(zip(*batch))

        # Tokenize and map tokens to indexes
        x = [self.vocab(DataModuleNews.tokenizer(text)) for text in x]

        # Bringing all samples to max_words length
        x = [
            (
                tokens + ([0] * (self.max_len - len(tokens)))
                if len(tokens) < self.max_len
                else tokens[: self.max_len]
            )
            for tokens in x
        ]

        return torch.tensor(x, dtype=torch.int32), torch.tensor(y)

    def train_dataloader(self) -> DataLoader:
        """
        Train DataLoader.

        :rtype: DataLoader
        :return DataLoader: train DataLoader
        """
        return DataLoader(
            self.train_dataset.data_to_loader,
            batch_size=self.batch_size,
            shuffle=True,
            collate_fn=self.vectorize_batch,
            num_workers=self.dataloader_num_workers,
        )

    def val_dataloader(self) -> DataLoader:
        """
        Val DataLoader.

        :rtype: DataLoader
        :return DataLoader: val DataLoader
        """
        return DataLoader(
            self.val_dataset.data_to_loader,
            batch_size=self.batch_size,
            shuffle=False,
            collate_fn=self.vectorize_batch,
            num_workers=self.dataloader_num_workers,
        )

    def predict_dataloader(self) -> DataLoader:
        """
        Test DataLoader.

        :rtype: DataLoader
        :return DataLoader: test DataLoader
        """
        return DataLoader(
            self.predict_dataset.data_to_loader,
            batch_size=self.batch_size,
            shuffle=False,
            collate_fn=self.vectorize_batch,
            num_workers=self.dataloader_num_workers,
        )
