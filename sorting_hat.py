#!/usr/bin/python3

from simanneal import Annealer
import random
import copy
import sys
import yaml

INFINITY = 10000
INVALID_CLASS_ID = -1

class Settings:
    num_members_in_each_team = []
    members = []

settings = Settings()

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
                if member not in self.preferences:
                    continue
                if self.preferences[member].class_affinity not in [INVALID_CLASS_ID, ti]:
                    v += INFINITY
                if len(team) < self.preferences[member].num_min_team_members:
                    v += INFINITY

        for hi, hist in enumerate(self.history):
            for ti, team in enumerate(self.state):
                if len(hist) <= ti:
                    continue
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
        return set()

    def get_other_members(self, member, team):
        if member not in team:
            return set()
        tmpTeam = copy.copy(team)
        tmpTeam.remove(member)
        return tmpTeam


def load_input(file_name):
    with open(file_name, 'r') as yml:
        config = yaml.safe_load(yml)

    load_settings(config['settings'])
    h = load_history(config['history'])
    p = load_preferences(config['preferences'])
    return h, p

def load_settings(input_settings):
    settings.num_members_in_each_team = input_settings['num_members_in_each_team']
    settings.members = input_settings['members']

    if sum(settings.num_members_in_each_team) != len(settings.members):
        print("invalid settings.")
        sys.exit(1)

def load_history(input_history):
    history = []
    for hist in input_history:
        tmpHist = []
        tmpTeam = set()
        for team in hist:
            for member in team:
                tmpTeam.add(member)
            tmpHist.append(copy.copy(tmpTeam))
            tmpTeam.clear()
        history.append(copy.copy(tmpHist))
        tmpHist.clear()

    return history

def load_preferences(input_preferences):
    preferences = dict()
    for pref in input_preferences:
        name = pref['name']
        if name not in settings.members:
            print("preference for invalid member '{}' found.".format(name))
            sys.exit(1)
        class_affinity = INVALID_CLASS_ID
        if 'class_affinity' in pref:
            class_affinity = pref['class_affinity']
        num_min_tream_members = 0
        if 'num_min_tream_members' in pref:
            num_min_tream_members = pref['num_min_tream_members']
        preferences[name] = Preference(class_affinity, num_min_tream_members)

    return preferences

def main():
    history, preferences = load_input(sys.argv[1])

    # initial assignment
    init_state = []
    membersIndex = 0
    for num_members in settings.num_members_in_each_team:
        tmpTeam = set()
        for i in range(num_members):
            tmpTeam.add(settings.members[membersIndex])
            membersIndex += 1
        init_state.append(copy.copy(tmpTeam))
        tmpTeam.clear()

    prob = SortingHat(init_state, preferences, history)
    prob.steps = 100000
    prob.copy_strategy = "deepcopy"
    prob.anneal()

    print()
    for i, team in enumerate(prob.state):
        print("team {}: {}".format(i, team))

if __name__ == '__main__':
    main()
