import json

from tqdm import tqdm

from app.config.document_filters import (
    BAD_PHRASES,
)
from app.services.retrieval.chunking_service import (
    ChunkingService,
)

from app.services.retrieval.voyage_embedding_service import (
    VoyageEmbeddingService,
)

from app.services.retrieval.faiss_service import (
    FAISSService,
)
from app.utils.pdf_loader import (
    PDFLoader,
)


RAW_DIR = "knowledge_base/raw"
OUTPUT_DIR = "knowledge_base"


BOOK_METADATA = {
    "AI Agents.pdf": {
        "title": "AI Agents",
        "domains": [
            "genai",
        ],
        "resource_type": "book",
    },

    "AI Engineering.pdf": {
        "title": "AI Engineering",
        "domains": [
            "genai",
            "mlops",
        ],
        "resource_type": "book",
    },

    "Data_Science_From_Scratch.pdf": {
        "title": (
            "Data Science From Scratch"
        ),
        "domains": [
            "data_science",
            "machine_learning",
        ],
        "resource_type": "book",
    },

    "Effective DevOps.pdf": {
        "title": (
            "Effective DevOps"
        ),
        "domains": [
            "backend",
            "devops",
        ],
        "resource_type": "book",
    },

    "Introducing MLOps.pdf": {
        "title": (
            "Introducing MLOps"
        ),
        "domains": [
            "mlops",
        ],
        "resource_type": "book",
    },

    "Learning DevOps.pdf": {
        "title": (
            "Learning DevOps"
        ),
        "domains": [
            "backend",
            "devops",
        ],
        "resource_type": "book",
    },

    "LLM Engineers Handbook.pdf": {
        "title": (
            "LLM Engineers Handbook"
        ),
        "domains": [
            "genai",
            "mlops",
        ],
        "resource_type": "book",
    },

    "Practical Statistics for Data Scientists.pdf": {
        "title": (
            "Practical Statistics for Data Scientists"
        ),
        "domains": [
            "data_science",
            "machine_learning",
        ],
        "resource_type": "book",
    },
}


def is_junk_chunk(
    chunk: str,
) -> bool:

    text = chunk.lower()

    for phrase in BAD_PHRASES:

        if phrase in text:
            return True

    return False


def keep_chunk(
    chunk: str,
) -> bool:

    if (
        len(
            chunk.split()
        )
        < 50
    ):
        return False

    if is_junk_chunk(
        chunk
    ):
        return False

    return True


def build_metadata(
    source_file,
    chunk_id,
):
    book_metadata = (
        BOOK_METADATA.get(
            source_file,
            {},
        )
    )

    return {
        "chunk_id": chunk_id,

        "source_file":
            source_file,

        "source_title":
            book_metadata.get(
                "title",
                source_file,
            ),

        "domains":
            book_metadata.get(
                "domains",
                [],
            ),

        "difficulty":
            "intermediate",

        "resource_type":
            book_metadata.get(
                "resource_type",
                "book",
            ),
    }


def main():

    pdf_files = (
        PDFLoader.get_pdf_files(
            RAW_DIR
        )
    )

    if not pdf_files:
        print(
            "No PDF files found."
        )
        return

    chunking_service = (
        ChunkingService()
    )


    embedding_service = (
    VoyageEmbeddingService()
    )

    all_chunks = []

    all_metadata = []

    chunk_id = 0

    for pdf_path in tqdm(
        pdf_files,
        desc="Processing PDFs",
    ):

        print(
            f"\nLoading: {pdf_path.name}"
        )

        text = (
            PDFLoader.load_pdf(
                str(pdf_path)
            )
        )

        chunks = (
            chunking_service
            .chunk_text(text)
        )

        kept_count = 0
        skipped_count = 0

        for chunk in chunks:

            if not keep_chunk(
                chunk
            ):
                skipped_count += 1
                continue

            all_chunks.append(
                chunk
            )

            metadata = (
                build_metadata(
                    source_file=(
                        pdf_path.name
                    ),
                    chunk_id=chunk_id,
                )
            )

            all_metadata.append(
                metadata
            )

            chunk_id += 1
            kept_count += 1

        print(
            f"Kept: {kept_count} | Skipped: {skipped_count}"
        )

    print(
        "\nGenerating embeddings..."
    )

    embeddings = (
        embedding_service
        .embed_texts(
            all_chunks
        )
    )

    print(
        "Creating FAISS index..."
    )

    faiss_service = (
        FAISSService(
            dimension=(
                embeddings.shape[1]
            )
        )
    )

    faiss_service.add_embeddings(
        embeddings
    )

    faiss_service.save(
        f"{OUTPUT_DIR}/faiss.index"
    )

    with open(
        f"{OUTPUT_DIR}/chunks.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            all_chunks,
            f,
            ensure_ascii=False,
            indent=2,
        )

    with open(
        f"{OUTPUT_DIR}/metadata.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            all_metadata,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(
        "\nKnowledge base successfully built."
    )

    print(
        f"Total chunks: {len(all_chunks)}"
    )


if __name__ == "__main__":
    main()