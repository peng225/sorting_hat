#!/usr/bin/python3

from simanneal import Annealer
import random
import copy
import sys

INFINITY = 10000


class SortingHat(Annealer):

    def __init__(self, init_state):
        super(SortingHat, self).__init__(init_state)

    def move(self):
        t1 = random.randint(0, len(self.state)-1)
        t2 = t1
        while t1 == t2:
            t2 = random.randint(0, len(self.state)-1)

        m1 = random.sample(self.state[t1], 1)[0]
        m2 = random.sample(self.state[t2], 1)[0]
        self.state[t1].remove(m1)
        self.state[t1].add(m2)
        self.state[t2].remove(m2)
        self.state[t2].add(m1)

    def energy(self):
        v = 0.0
        for hi, hist in enumerate(history):
            for ti, team in enumerate(self.state):
                for member in team:
                    if member in hist[ti]:
                        v += (hi+2.0)/(hi+1.0)

                if affinity[member] != -1 and affinity[member] != ti:
                    v += INFINITY

                other_members = self.get_other_members(member, team)
                past_team = self.find_team(member, hist)
                past_other_members = self.get_other_members(member, past_team)
                intersect = other_members & past_other_members
                v += (hi+2.0)/(hi+1.0)*len(intersect)
        return v

    def find_team(self, member, teams):
        for team in teams:
            if member in team:
                return team
        print("team not found for {}.".format(team))
        sys.exit(1)

    def get_other_members(self, member, team):
        tmpTeam = copy.copy(team)
        tmpTeam.remove(member)
        return tmpTeam


if __name__ == '__main__':
    num_teams = 3
    num_members = 8
    teams = [i for i in range(num_teams)]
    members = [i for i in range(num_members)]
    history = []
    history.append([{0, 1, 2}, {3, 4}, {5, 6, 7}])
    history.append([{0, 3, 5}, {1, 7}, {2, 4, 6}])
    history.append([{0, 2, 6}, {3, 5}, {1, 4, 7}])

    # initial assignment
    init_state = []
    init_state.append({0, 1, 2})
    init_state.append({3, 4})
    init_state.append({5, 6, 7})

    affinity = [-1, -1, -1, -1, 2, -1, -1, -1]

    prob = SortingHat(init_state)
    prob.steps = 100000
    prob.copy_strategy = "deepcopy"
    prob.anneal()

    print(prob.state)
