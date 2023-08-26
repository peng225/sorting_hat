#!/usr/bin/python3

import random
import copy
import sys
from simanneal import Annealer
import evaluator
import input_handler

INFINITY = 10000

class SortingHat(Annealer):
    ev = evaluator.Evaluator({}, [], [])
    settings = input_handler.Settings()

    def __init__(self, init_state, ev, settings):
        super().__init__(init_state)
        self.ev = ev
        self.settings = settings

    def move(self):
        ti1 = random.randint(0, len(self.state)-1)
        ti2 = ti1
        while ti1 == ti2:
            ti2 = random.randint(0, len(self.state)-1)

        m1 = random.sample(self.state[ti1], 1)[0]
        m2 = random.sample(self.state[ti2], 1)[0]
        self.state[ti1].remove(m1)
        self.state[ti1].add(m2)
        self.state[ti2].remove(m2)
        self.state[ti2].add(m1)

    def energy(self):
        return self.ev.evaluate(self.state)

    def show_result(self):
        print()
        print()
        print("result:")
        print(f"value: {self.best_energy}")
        for i, team in enumerate(self.best_state):
            print(f"team {i}: {team}")

def generate_initial_state(settings):
    init_state = []
    tmp_members = copy.copy(settings.members)
    for num_members in settings.num_members_in_each_team:
        tmp_team = set()
        for _ in range(num_members):
            tmp_team.add(tmp_members.pop())
        init_state.append(copy.copy(tmp_team))
    return init_state

def main():
    settings, history, preferences = input_handler.load(sys.argv[1])
    init_state = generate_initial_state(settings)
    ev = evaluator.Evaluator(preferences, history, settings.num_remaining_members_in_each_team)
    sh = SortingHat(init_state, ev, settings)
    sh.steps = 100000
    sh.copy_strategy = "deepcopy"
    sh.anneal()
    sh.show_result()

if __name__ == '__main__':
    main()
