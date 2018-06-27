from random import uniform

from action import Action
from field import Field
from markov_decision_process import MarkovDecisionProcess


def main():
    mdp:MarkovDecisionProcess = MarkovDecisionProcess()
    mdp.set_field(1, 1, Field.OBSTACLE)
    mdp.set_field(3, 2, Field.POS_TERMINAL)
    mdp.set_field(3, 1, Field.NEG_TERMINAL)
    print(mdp)

    while not mdp.terminated:
        actions = mdp.get_possible_actions()
        action = actions[int(uniform(0, len(actions)))]
        mdp.act(action)
        print(str(mdp))

    actions = mdp.get_possible_actions()
    action = actions[int(uniform(0, len(actions)))]
    mdp.act(action)
    print(mdp)


if __name__ == "__main__":
    main()