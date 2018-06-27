from action import Action
from markov_decision_process import MarkovDecisionProcess


class QLearner:

    def __init__(self, mdp:MarkovDecisionProcess):
        """
        Creates a Q Learning object with the given MDP.
        :param mdp: The MDP on which Q Learning will be happening.
        """
        self.mdp:MarkovDecisionProcess = mdp
        self.q_values = {((int,int),Action):float}  # key=(State,Action) value=q_value


    def step(self):
        pass