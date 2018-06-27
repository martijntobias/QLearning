from enum import Enum

class Field(Enum):

    EMPTY = "."
    OBSTACLE = "X"
    POS_TERMINAL = "+"
    NEG_TERMINAL = "-"


    def __str__(self) -> str:
        return self.value