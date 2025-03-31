import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset


class TextDataset(Dataset):
    def __init__(self, text_data: pd.DataFrame):
        super().__init__()

        self.text_data = text_data

    def __len__(self) -> int:
        return len(self.text_data)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        if torch.is_tensor(idx):
            idx = idx.tolist()

        row = self.text_data.iloc[idx]
        features = torch.tensor([row["test"]])
        label = torch.tensor([row["sentiment"]], dtype=torch.long)

        return {"features": features, "label": label}
