import os
from pathlib import Path
from typing import List

from core.models import PuzzleConfig

ASSETS_DIR = Path(os.path.dirname(os.path.dirname(__file__)))
IMAGES_DIR = ASSETS_DIR / "assets" / "images"

DEFAULT_TITLES = [
    "Panda Hello",
    "Peach Kitty",
    "Chilly Chibi",
    "Lazy White",
    "Koala Hug",
    "Fluffy Cat",
    "Black Hair Chibi",
    "Jujutsu Kaisen",
    "Sky Eyes",
    "Happy Shroom",
]

DIFFICULTY_PRESETS = [
    (4, 5),
    (4, 5),
    (4, 5),
]


def _natural_key(filename: str) -> int:
    """Sort image filenames like 1,2,10 instead of 1,10,2."""
    stem = Path(filename).stem
    try:
        return int(stem)
    except ValueError:
        return 0


def _discover_images(limit: int = 10) -> List[str]:
    if not IMAGES_DIR.exists():
        return []
    files = [f.name for f in IMAGES_DIR.iterdir() if f.is_file()]
    files.sort(key=_natural_key)
    return files[:limit]


def build_image_catalog(limit: int = 10) -> List[PuzzleConfig]:
    catalog: List[PuzzleConfig] = []
    files = _discover_images(limit)
    for idx, filename in enumerate(files):
        rows, cols = DIFFICULTY_PRESETS[idx % len(DIFFICULTY_PRESETS)]
        title = DEFAULT_TITLES[idx % len(DEFAULT_TITLES)]
        catalog.append(
            PuzzleConfig(
                id=f"puzzle_{idx+1}",
                title=title,
                image_path=str(IMAGES_DIR / filename),
                rows=rows,
                cols=cols,
            )
        )
    return catalog


IMAGE_CATALOG = build_image_catalog()
IMAGE_LIST = [Path(config.image_path).name for config in IMAGE_CATALOG]


def image_path(name: str) -> str:
    return str(IMAGES_DIR / name)