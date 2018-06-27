from _ast import List

from random import uniform

from action import Action
from field import Field


class MarkovDecisionProcess:


    def __init__(self, x:int=4, y:int=3, rew_empty:float=-.04, rew_pos:float=1, rew_neg:float=-1, failure:float=.2):
        """
        Creates a Markov Decision Problem with the given values. All fields are set to empty and the starting position
        is set to (0, 0). The agent's position are initialized to (0, 0) as well.
        :param x: The width of the MDP world. Default 4.
        :param y: The height of the MDP world. Default 4.
        :param rew_empty: The reward for visiting an empty field. Default -0.04.
        :param rew_pos: The reward for ending on a positive terminal. Default 1.
        :param rew_neg: The reward for ending on a negative terminal. Default -1.
        :param failure: The chance of failing an action. When failed, the action that will actually occur will be
        a fifty-fifty chance of moving clockwise or counterclockwise relative to the attempted action.
        """
        self.fields:[[Field]] = []
        for i in range(x):
            self.fields.append([])
            for j in range(y):
                self.fields[i].append(Field.EMPTY)

        self.rew_empty:float = rew_empty
        self.rew_pos:float = rew_pos
        self.rew_neg:float = rew_neg

        self.failure:float = failure

        self.start_x:int = 0
        self.start_y:int = 0

        self.agent_x:int = self.start_x
        self.agent_y:int = self.start_y

        self.terminated = False  # wether or not the Agent has taken the Terminate Action from a Terminal meaniung the
                                 # MDP must be restarted.


    def set_field(self, x:int, y:int, field:Field) -> None:
        """
        Sets the given coord in this MDP to be the given Field
        :param x: The x-coord of the field to be set.
        :param y: The y-coord of the field to be set.
        :param field: The Field value the given coord will be set to.
        """
        self.fields[x][y] = field


    def set_start_coords(self, x:int, y:int) -> None:
        """
        Sets the starting coords of the agent. This will be where the agent will be moved to when the MDP is reset
        either manually or after the agent takes an action from a terminal field. Note that this will do nothing if the
        MDP is not reset afterwards,
        :param x: The x-coord of the new starting coords.
        :param y: The y-coord of the new starting coords.
        """
        self.start_x = x
        self.start_y = y


    def restart(self):
        """
        Resets the Agent to the starting coords.
        :return:
        """
        self.agent_x = self.start_x
        self.agent_y = self.start_y
        self.terminated = False


    def act(self, action:Action) -> None:
        """
        Takes an actiom, which may fail and result in a different direction. If the Action would result in the Agent
        leaving the map or colliding with an obstacle, the agent will stay in its place.
        :param action: The Action this agent will try to perform.
        """
        if self.terminated:
            self.restart()

        if action == Action.TERMINAL:
            self.terminated = True

        if uniform(0, 1) < self.failure:
            action = action.turn(uniform(0, 1) <= 0.5)  # clockwise or counter-clockwise with equal chance for both

        dx, dy = action.delta()
        x, y = self.agent_x+dx, self.agent_y+dy

        if x < 0 or x >= len(self.fields) or y < 0 or y >= len(self.fields[0]) or self.fields[x][y] == Field.OBSTACLE:
            return

        self.agent_x = x
        self.agent_y = y


    def get_reward(self) -> float:
        """
        Returns the reward of the Field the Agent is currently standing on.
        :return: The reward of the Field the Agent is standing on.
        """
        field = self.fields[self.agent_x][self.agent_y]
        if field == Field.EMPTY:
            return self.rew_empty
        elif field == Field.POS_TERMINAL:
            return self.rew_pos
        elif field == Field.NEG_TERMINAL:
            return self.rew_neg

        raise ValueError  # Agent is standing on an illegal tile!


    def get_possible_actions(self) -> [Action]:
        """
        Will return the possible Actions. In essence, this will {TERMINAL} if the agent entered a terminal field and
        needs to "exit" it. If this has already been done, the MDP is not yet restarted, so the Agent is still there.
        However, the regular actions will be returned regardles, because the MDP will restart at the start of the next
        act() call.
        :return: The list of Actions the Agent can perform, including Actions that would result in walking into a wall.
        """
        if self.fields[self.agent_x][self.agent_y] == Field.EMPTY or self.terminated:
            return [Action.NORTH, Action.EAST, Action.SOUTH, Action.WEST]
        else:  # must be terminal
            return [Action.TERMINAL]



    def __str__(self) -> str:
        """
        Returns a visualization of the MDP to the console. X being an obstacle, + a positive terminal, - a negative
        terminal, . an empty field, a @ the agent regardless of what tile he is on. Has a border on top and on the
        side.
        """
        ret_string:str = ""

        border:str = "-" * (len(self.fields) + 2)
        ret_string += border

        for y in range(len(self.fields[0])-1, -1, -1):  # loop other way around to display bottom as y=0
            line:str = "\n|"
            for x in range(len(self.fields)):
                if x == self.agent_x and y == self.agent_y:
                    line += "@"
                else:
                    line += str(self.fields[x][y])
            line += "|"
            ret_string += line

        return ret_string



