import ast
from typing import List, Dict


def parse_python_file(file_path: str) -> List[Dict]:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    source_lines = source.splitlines()
    parsed_elements = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start = node.lineno
            end = getattr(node, "end_lineno", start)

            code_snippet = "\n".join(source_lines[start - 1 : end])

            parsed_elements.append(
                {
                    "type": "function",
                    "name": node.name,
                    "content": code_snippet,
                    "start_line": start,
                    "end_line": end,
                }
            )

        elif isinstance(node, ast.ClassDef):
            start = node.lineno
            end = getattr(node, "end_lineno", start)

            code_snippet = "\n".join(source_lines[start - 1 : end])

            parsed_elements.append(
                {
                    "type": "class",
                    "name": node.name,
                    "content": code_snippet,
                    "start_line": start,
                    "end_line": end,
                }
            )

    return parsed_elements
