from enum import Enum

class Action(Enum):

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    TERMINAL = 4


    def turn(self, clockwise:bool):
        """
        Returns the Action you get when turning this action either clockwise or counter-clockwise. Will return this
        the terminal action if this is the terminal action.
        :param clockwise: Wether the movement is clockwise. If false, it will be counter-clockwise.
        :return: An Action that represents the direction of this Action but turned in the given direction.
        """
        if self == Action.TERMINAL:
            return Action.TERMINAL

        if clockwise:
            if self == Action.WEST:
                return Action.NORTH
            else:
                return Action(self.value+1)
        else:
            if self == Action.NORTH:
                return Action.WEST
            else:
                return Action(self.value-1)


    def delta(self) -> (int, int):
        """
        Returns a tuple with a difference in x and y taking this action will result in.
        :return: (dx, dy)
        """
        if self == Action.NORTH:
            return 0, 1
        elif self == Action.EAST:
            return 1, 0
        elif self == Action.SOUTH:
            return 0, -1
        elif self == Action.WEST:
            return -1, 0
        elif self == Action.TERMINAL:
            return 0, 0
