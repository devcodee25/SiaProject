class GameState:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.moves = 0
        self.elapsed_seconds = 0

    def configure(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.reset()

    def increment_move(self):
        self.moves += 1

    def reset(self):
        self.moves = 0
        self.elapsed_seconds = 0

    def reset_moves_only(self):
        self.moves = 0

    def tick(self):
        self.elapsed_seconds += 1

    def formatted_time(self) -> str:
        minutes, seconds = divmod(self.elapsed_seconds, 60)
        return f"{minutes:02}:{seconds:02}"