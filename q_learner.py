from random import Random
from time import time

from action import Action
from field import Field
from markov_decision_process import MarkovDecisionProcess


class QLearner:

    def __init__(self, mdp:MarkovDecisionProcess, learning_rate:float=0.5, discount_factor:float=0.9):
        """
        Creates a Q Learning object with the given MDP, learning rate, and discount factor.
        :param mdp: The MDP on which Q Learning will be happening.
        """
        self.mdp:MarkovDecisionProcess = mdp
        self.learning_rate:float = learning_rate
        self.discount_factor:float = discount_factor

        self.q_values = {((int,int),Action):float}  # key=(State,Action) value=q_value


    def print_actions(self):
        # debug
        for action in self.mdp.get_possible_actions():
            key = (self.mdp.agent_x, self.mdp.agent_y), action
            if key in self.q_values:
                print(self.q_values[key], "\t", action)
            else:
                print(0, "\t", action)


    def step(self):
        """
        Takes one step, either randomly or not depending on the initialization of this object, and update its q values.
        """
        state:(int,int) = (self.mdp.agent_x, self.mdp.agent_y)
        possible_actions:[Action] = self.mdp.get_possible_actions()

        # initialize default q_values when needed, and look up actions with highest q_values
        q_max:float = -1e500  # -inf
        actions_max:[Action] = []

        for action in possible_actions:
            key:((int,int), Action) = (state, action)
            if key not in self.q_values:
                self.q_values[key] = 0
            if self.q_values[key] > q_max:
                q_max = self.q_values[key]
                actions_max = [action]
            elif self.q_values[key] == q_max:
                actions_max.append(action)

        #  always break ties in same order
        chosen_action:Action
        for action in [Action.NORTH, Action.EAST, Action.SOUTH, Action.WEST, Action.TERMINAL]:
            if action in actions_max:
                chosen_action = action
                break

        print("choose", chosen_action, "from", actions_max)

        self.mdp.act(chosen_action)

        observed_reward:float = self.mdp.get_reward()
        old_q:float = self.q_values[(state, chosen_action)]
        new_q:float = old_q + self.learning_rate * \
                      (observed_reward + self.discount_factor * self.max_q(self.mdp.agent_x, self.mdp.agent_y) - old_q)
        self.q_values[(state, chosen_action)] = new_q

    def max_q(self, x:int, y:int):
        """
        Returns the max q value for the given location. Will return 0 if the agent knows nothing about this location.
        :param x: x-coord from which the highest q will be given.
        :param y: y-coord from which the highest q will be given
        :return: the highest q value from the given coord
        """
        max_q:float = None
        for action in [Action.NORTH, Action.EAST, Action.SOUTH, Action.WEST, Action.TERMINAL]:
            key:((int,int),Action) = ((x, y), action)
            if key not in self.q_values:
                break
            q:float = self.q_values[key]
            if max_q is None or q > max_q:
                max_q = q

        return 0 if max_q is None else max_q

    def __str__(self):
        """
        Returns a string representation of the MDP with the q values for each action
        :return:
        """
        ret_string: str = ""

        border: str = "-" * (len(self.mdp.fields)*8 + 1)
        ret_string += border

        for y in range(len(self.mdp.fields[0]) - 1, -1, -1):  # loop other way around to display bottom as y=0
            row = ""
            for i in range(7):  # string representation is 5 rows
                row += "\n|"
                for x in range(len(self.mdp.fields)):
                    row += self.str_row(x, y, i) + "|"
            ret_string += row + "\n" + border

        return ret_string

    def str_row(self, x:int, y:int, i:int):
        """
        Returns the row of the string representation of this.   '%012.1f' % v
        :param x:
        :param y:
        :param i:
        :return:
        """
        field:Field = self.mdp.fields[x][y]
        state:(int,int) = self.mdp.agent_x, self.mdp.agent_y

        ret_str:str
        str_list: [str]

        if field == Field.OBSTACLE:
            str_list = list("\\     /"
                            " \\   / "
                            "  \\ /  "
                            "   X   "
                            "  / \\  "
                            " /   \\ "
                            "/     \\"[i*7:i*7+7])

        elif field == Field.NEG_TERMINAL:
            str_list = "\\+++++/" \
                       "+X   X+" \
                       "+| 1 |+" \
                       "+|234|+" \
                       "+|   |+" \
                       "+X---X+" \
                       "/+++++\\"[i*7:i*7+7]
            key:((int,int),Action) = state, Action.TERMINAL
            val:float = self.q_values[key] if key in self.q_values else 0
            str_list
            dict:{str:str} = {"1":"+" if val >= 0 else "-",
                              "234":}
            [dic.get(n, n) for n in a]

        elif field == Field.POS_TERMINAL:
            str_list = "\\-----/" \
                       "-X   X-" \
                       "-| 1 |-" \
                       "-|234|-" \
                       "-|   |-" \
                       "-X---X-" \
                       "/-----\\"[i*7:i*7+7]

        elif field == Field.EMPTY:
            str_list = "\\ 1234/" \
                       " \   / " \
                       "5 \\ /6 " \
                       "789XABC" \
                       "  / \\  " \
                       " /   \\ " \
                       "/ DEFG\\"[i*7:i*7+7]

        return "".join(str_list)
