from pathlib import Path


def get_files(path_in: str) -> dict[str, float]:
    path = Path(path_in)

    if not path.exists():
        return dict()

    items = {}

    for file in path.iterdir():
        if not file.is_file():
            continue

        items[file.name] = file.stat().st_mtime

    return items
