import numpy as np
import voyageai

from app.core.config.settings import (
    settings,
)


class VoyageEmbeddingService:

    def __init__(
        self,
    ):
        self.client = (
            voyageai.Client(
                api_key=(
                    settings
                    .VOYAGE_API_KEY
                )
            )
        )

        self.model = (
            "voyage-3"
        )

    def embed_texts(
        self,
        texts: list[str],
        batch_size: int = 128,
    ):

        all_embeddings = []

        total = len(texts)

        for i in range(
            0,
            total,
            batch_size,
        ):

            batch = texts[
                i : i + batch_size
            ]

            response = (
                self.client.embed(
                    batch,
                    model=self.model,
                    input_type=(
                        "document"
                    ),
                )
            )

            all_embeddings.extend(
                response.embeddings
            )

            processed = min(
                i + batch_size,
                total,
            )

            print(
                f"Embedded "
                f"{processed}"
                f"/{total}"
            )

        return np.array(
            all_embeddings,
            dtype="float32",
        )

    def embed_query(
        self,
        query: str,
    ):

        response = (
            self.client.embed(
                [query],
                model=self.model,
                input_type=(
                    "query"
                ),
            )
        )

        return np.array(
            response.embeddings[0],
            dtype="float32",
        )