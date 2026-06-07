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
    def load_pdf(
        file_path: str,
    ) -> str:

        reader = PdfReader(
            file_path
        )

        file_name = (
            Path(file_path).name
        )

        text = []

        for (
            page_number,
            page,
        ) in enumerate(
            reader.pages,
            start=1,
        ):

            if (
                PDFLoader
                .should_skip_page(
                    file_name,
                    page_number,
                )
            ):
                continue

            extracted = (
                page.extract_text()
            )

            if extracted:
                text.append(
                    extracted
                )

        return "\n".join(text)

    @staticmethod
    def get_pdf_files(
        directory: str,
    ):
        return list(
            Path(directory).glob(
                "*.pdf"
            )
        )