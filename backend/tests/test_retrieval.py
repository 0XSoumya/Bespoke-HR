import json

import faiss
import numpy as np

from app.services.retrieval.voyage_embedding_service import (
    VoyageEmbeddingService,
)


TOP_K = 5


def main():

    with open(
        "knowledge_base/chunks.json",
        "r",
        encoding="utf-8",
    ) as f:

        chunks = json.load(f)

    index = faiss.read_index(
        "knowledge_base/faiss.index"
    )

    embedding_service = (
        VoyageEmbeddingService()
    )

    while True:

        query = input(
            "\nQuery: "
        )

        if (
            query.lower()
            == "exit"
        ):
            break

        query_embedding = (
            embedding_service
            .embed_query(
                query
            )
        )

        print(
            f"\nQuery Embedding Shape: "
            f"{query_embedding.shape}"
        )

        print(
            f"FAISS Dimension: "
            f"{index.d}"
        )

        scores, indices = (
            index.search(
                np.array(
                    [query_embedding]
                ).astype(
                    "float32"
                ),
                TOP_K,
            )
        )

        print(
            "\nTop Results:\n"
        )

        for rank, idx in enumerate(
            indices[0]
        ):

            print(
                f"Result {rank + 1}"
            )

            print(
                "-" * 50
            )

            print(
                chunks[idx][:1000]
            )

            print("\n")


if __name__ == "__main__":
    main()