#!/usr/bin/python3

import copy
import sys
import evaluator
import input_handler

INFINITY = 10000000

class SortingHatBruteForce():
    ev: evaluator.Evaluator
    settings: input_handler.Settings
    state = []
    best_state = []
    best_energy = 0

    def __init__(self, ev, settings):
        self.ev = ev
        self.settings = settings

    def search(self):
        self.best_state = []
        self.best_energy = INFINITY
        self.state = [set() for i in range(len(self.settings.num_members_in_each_team))]
        current_num_members_in_each_team = copy.copy(self.settings.num_members_in_each_team)
        current_members = copy.copy(self.settings.members)
        self.search_helper(current_num_members_in_each_team, current_members)

    def search_helper(self, current_num_members_in_each_team, current_members):
        if sum(current_num_members_in_each_team) == 0:
            v = self.ev.evaluate(self.state)
            if v < self.best_energy:
                self.best_state = copy.deepcopy(self.state)
                self.best_energy = v
            return

        for i, _ in enumerate(current_num_members_in_each_team):
            if current_num_members_in_each_team[i] == 0:
                continue
            current_num_members_in_each_team[i] = current_num_members_in_each_team[i] - 1
            tmp_member = current_members.pop()
            self.state[i].add(tmp_member)
            self.search_helper(current_num_members_in_each_team, current_members)
            self.state[i].remove(tmp_member)
            current_members.add(tmp_member)
            current_num_members_in_each_team[i] = current_num_members_in_each_team[i] + 1

    def show_result(self):
        print("result:")
        print(f"value: {self.best_energy}")
        for i, team in enumerate(self.best_state):
            print(f"team {i}: {team}")

def main():
    settings, history, preferences = input_handler.load(sys.argv[1])
    ev = evaluator.Evaluator(preferences, history, settings.num_remaining_members_in_each_team)
    shbf = SortingHatBruteForce(ev, settings)
    shbf.search()
    shbf.show_result()

if __name__ == '__main__':
    main()
