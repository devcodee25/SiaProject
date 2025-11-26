from dataclasses import dataclass


@dataclass(frozen=True)
class PuzzleConfig:
    id: str
    title: str
    image_path: str
    rows: int
    cols: int

    @property
    def piece_count(self) -> int:
        return self.rows * self.cols


