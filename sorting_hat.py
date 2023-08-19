#!/usr/bin/python3

from simanneal import Annealer
import random
import copy
import sys

INFINITY = 10000
INVALID_CLASS_ID = -1

class Preference:
    class_affinity = INVALID_CLASS_ID
    num_min_team_members = 0

    def __init__(self, class_affinity=INVALID_CLASS_ID, num_min_team_members=0):
        self.class_affinity = class_affinity
        self.num_min_team_members = num_min_team_members

class SortingHat(Annealer):
    preferences = dict()
    history = list()

    def __init__(self, init_state, preferences, history):
        super(SortingHat, self).__init__(init_state)
        self.preferences = preferences
        self.history = history

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
        v = 0.0
        for ti, team in enumerate(self.state):
            for member in team:
                if self.preferences[member].class_affinity not in [INVALID_CLASS_ID, ti]:
                    v += INFINITY
                if len(team) < self.preferences[member].num_min_team_members:
                    v += INFINITY

        for hi, hist in enumerate(self.history):
            for ti, team in enumerate(self.state):
                for member in team:
                    if member in hist[ti]:
                        v += (hi+2.0)/(hi+1.0)

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


def main():
    num_teams = 3
    num_members = 8
    teams = [i for i in range(num_teams)]
    members = [i for i in range(num_members)]
    history = []
    history.append([{"taro", "jiro", "saburo"}, {"kenta", "takashi"}, {"takuya", "hayato", "masao"}])
    history.append([{"taro", "kenta", "takuya"}, {"jiro", "masao"}, {"saburo", "takashi", "hayato"}])
    history.append([{"taro", "saburo", "hayato"}, {"kenta", "takuya"}, {"jiro", "takashi", "masao"}])

    # initial assignment
    init_state = []
    init_state.append({"taro", "jiro", "saburo"})
    init_state.append({"kenta", "takashi"})
    init_state.append({"takuya", "hayato", "masao"})

    preferences = {
        "taro": Preference(num_min_team_members=3),
        "jiro": Preference(num_min_team_members=3),
        "saburo": Preference(),
        "kenta": Preference(),
        "takashi": Preference(class_affinity=2),
        "takuya": Preference(),
        "hayato": Preference(),
        "masao": Preference(),
    }

    prob = SortingHat(init_state, preferences, history)
    prob.steps = 100000
    prob.copy_strategy = "deepcopy"
    prob.anneal()

    print()
    for i, team in enumerate(prob.state):
        print("team {}: {}".format(i, team))

if __name__ == '__main__':
    main()
