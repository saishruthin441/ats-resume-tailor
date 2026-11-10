"""
Resume and Job Description Text Parser.
Supports PDF and DOCX files, falls back to plain text.
"""

from pathlib import Path


def extract_text(file_path: Path) -> str:
    """
    Extract plain text from a resume file.
    Supports: .pdf, .docx, .txt
    """
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(str(file_path))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            raise RuntimeError("pypdf not installed. Run: pip install pypdf")

    elif suffix == ".docx":
        try:
            import docx2txt
            return docx2txt.process(str(file_path))
        except ImportError:
            raise RuntimeError("docx2txt not installed. Run: pip install docx2txt")

    elif suffix == ".txt":
        return file_path.read_text(encoding="utf-8")

    else:
        raise ValueError(f"Unsupported file format: {suffix}. Use .pdf, .docx, or .txt")
