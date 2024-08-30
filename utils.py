class Position:
    def __init__(self, row: int, column: int):
        """
        Represent a location on the board
        """
        self.row = row
        self.column = column

    def __add__(self, other: "Position") -> "Position":
        row = self.row + other.row
        col = self.column + other.column
        return Position(row, col)

    def __sub__(self, other: "Position") -> "Position":
        row = self.row - other.row
        col = self.column - other.column
        return Position(row, col)

    def __hash__(self) -> int:
        return hash((self.row, self.column))

    def __eq__(self, other: "Position") -> bool:
        return self.row == other.row and self.column == other.column

    def __str__(self) -> str:
        return f"({self.row},{self.column})"

    def __repr__(self) -> str:
        return f"({self.row},{self.column})"
