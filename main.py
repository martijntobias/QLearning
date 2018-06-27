from random import uniform

from action import Action
from field import Field
from markov_decision_process import MarkovDecisionProcess
from q_learner import QLearner


def main():
    mdp:MarkovDecisionProcess = MarkovDecisionProcess()
    mdp.set_field(1, 1, Field.OBSTACLE)
    mdp.set_field(3, 2, Field.POS_TERMINAL)
    mdp.set_field(3, 1, Field.NEG_TERMINAL)
    print(mdp)

    q_learner:QLearner = QLearner(mdp)

    while True:
        if mdp.terminated:
            mdp.restart()
        q_learner.print_actions()
        input("enter to advance")
        q_learner.step()
        print(q_learner)


if __name__ == "__main__":
    main()