import gc
import re
import warnings
from copy import deepcopy

import numpy as np
import pandas as pd
from natasha import (
    Doc,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsNERTagger,
    Segmenter,
)
from tqdm.auto import tqdm

warnings.filterwarnings("ignore")
