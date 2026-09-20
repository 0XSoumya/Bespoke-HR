from pathlib import Path

from pypdf import PdfReader

from app.config.document_filters import (
    DOCUMENT_FILTERS,
)


class PDFLoader:
    @staticmethod
    def should_skip_page(
        file_name: str,
        page_number: int,
    ) -> bool:

        config = (
            DOCUMENT_FILTERS.get(
                file_name,
                {},
            )
        )

        ranges = config.get(
            "skip_ranges",
            [],
        )

        for (
            start,
            end,
        ) in ranges:

            if (
                start
                <= page_number
                <= end
            ):
                return True

        return False

    @staticmethod
    def load_pdf_from_bytes(
        content: bytes,
        file_name: str = "document.pdf",
    ) -> str:
        import io
        if not content.startswith(b"%PDF-"):
            raise ValueError("File does not have a valid PDF header (%PDF-)")

        try:
            reader = PdfReader(io.BytesIO(content))
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {e}")

        if reader.is_encrypted:
            raise ValueError("Encrypted or password-protected PDFs are not supported")

        text = []
        for page_number, page in enumerate(reader.pages, start=1):
            if PDFLoader.should_skip_page(file_name, page_number):
                continue
            extracted = page.extract_text()
            if extracted:
                text.append(extracted)

        full_text = "\n".join(text).strip()
        if not full_text:
            raise ValueError("No readable text could be extracted from the PDF. It may be empty or an image scan.")
        return full_text

    @staticmethod
    def load_pdf(
        file_path: str,
    ) -> str:
        path = Path(file_path)
        with open(path, "rb") as f:
            content = f.read()
        return PDFLoader.load_pdf_from_bytes(content, file_name=path.name)

    @staticmethod
    def get_pdf_files(
        directory: str,
    ):
        return list(
            Path(directory).glob(
                "*.pdf"
            )
        )