import faiss
import numpy as np
from pathlib import Path


class FAISSService:
    def __init__(
        self,
        dimension: int,
    ):
        self.index = (
            faiss.IndexFlatIP(
                dimension
            )
        )

    def add_embeddings(
        self,
        embeddings: np.ndarray,
    ):
        self.index.add(
            embeddings.astype(
                "float32"
            )
        )

    def save(
        self,
        path: str,
    ):
        Path(path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            path,
        )

    @staticmethod
    def load(path: str):
        return faiss.read_index(
            path
        )