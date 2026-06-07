from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-base-en-v1.5"
        )

    def embed_texts(
        self,
        texts: list[str],
    ):
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

    def embed_query(
        self,
        query: str,
    ):
        return self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]