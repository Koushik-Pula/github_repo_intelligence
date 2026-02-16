from typing import List, Dict
import os


def create_code_chunks(
    parsed_elements: List[Dict],
    file_path: str,
    language: str = "python",
) -> List[Dict]:
    """
    Convert parsed code elements into RAG-ready chunks.
    """

    chunks = []
    file_name = os.path.basename(file_path)

    for element in parsed_elements:
        chunk = {
            "page_content": element["content"],
            "metadata": {
                "file": file_name,
                "symbol": element.get("name"),
                "symbol_type": element.get("type"),
                "language": language,
                "start_line": element.get("start_line"),
                "end_line": element.get("end_line"),
            },
        }
        chunks.append(chunk)

    return chunks
