#!/usr/bin/python3

from simanneal import Annealer
import random
import copy
import sys
import evaluator
import input

INFINITY = 10000

class SortingHatBruteForce():
    ev = evaluator.Evaluator(dict(), [])
    state = []
    best_state = []
    best_energy = 0

    def __init__(self, ev):
        self.ev = ev

    def search(self):
        self.best_state = []
        self.best_energy = INFINITY*100
        self.state = [set() for i in range(len(input.settings.num_members_in_each_team))]
        current_num_members_in_each_team = copy.copy(input.settings.num_members_in_each_team)
        current_members = copy.copy(input.settings.members)
        self.search_helper(current_num_members_in_each_team, current_members)

    def search_helper(self, current_num_members_in_each_team, current_members):
        if sum(current_num_members_in_each_team) == 0:
            v = self.ev.evaluate(self.state)
            if v < self.best_energy:
                self.best_state = copy.deepcopy(self.state)
                self.best_energy = v
            return

        for i in range(len(current_num_members_in_each_team)):
            if current_num_members_in_each_team[i] == 0:
                continue
            current_num_members_in_each_team[i] = current_num_members_in_each_team[i] - 1
            tmp_member = current_members.pop()
            self.state[i].add(tmp_member)
            self.search_helper(current_num_members_in_each_team, current_members)
            self.state[i].remove(tmp_member)
            current_members.add(tmp_member)
            current_num_members_in_each_team[i] = current_num_members_in_each_team[i] + 1

def show_result(state):
    print("result:")
    for i, team in enumerate(state):
        print("team {}: {}".format(i, team))

def main():
    history, preferences = input.load(sys.argv[1])
    ev = evaluator.Evaluator(preferences, history)
    shbf = SortingHatBruteForce(ev)
    shbf.search()
    show_result(shbf.best_state)

if __name__ == '__main__':
    main()
