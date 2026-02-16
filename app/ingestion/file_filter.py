import os

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".idea",
    ".vscode",
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}

MAX_FILE_SIZE_BYTES = 1_000_000

def is_valid_file(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return False

    try:
        if os.path.getsize(file_path) > MAX_FILE_SIZE_BYTES:
            return False
    except OSError:
        return False

    return True

def collect_source_files(repo_path: str) -> list[str]:
    collected_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            file_path = os.path.join(root, file)

            if is_valid_file(file_path):
                collected_files.append(file_path)

    return collected_files