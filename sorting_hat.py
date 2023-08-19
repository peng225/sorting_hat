#!/usr/bin/python3

from simanneal import Annealer
import random
import copy
import sys
import yaml

INFINITY = 10000
DECAY_RATE = 0.9

class Settings:
    num_members_in_each_team = []
    num_remaining_members_in_each_team = []
    members = set()

settings = Settings()

class Preference:
    class_anti_affinity = set()
    num_min_team_members = 0

    def __init__(self, class_anti_affinity, num_min_team_members):
        self.class_anti_affinity = class_anti_affinity
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
        # Check constraints.
        # When a constraint is violated, a very large value is added to the energy.
        for ti, team in enumerate(self.state):
            for member in team:
                if member not in self.preferences:
                    continue
                if ti in self.preferences[member].class_anti_affinity:
                    v += INFINITY
                if len(team) < self.preferences[member].num_min_team_members:
                    v += INFINITY
            
            if len(self.history) == 0 or len(self.history) <= ti:
                continue

            prev_team = self.history[0][ti]
            if len(team & prev_team) < settings.num_remaining_members_in_each_team[ti]:
                v += INFINITY

        for hi, past_teams in enumerate(self.history):
            for ti, team in enumerate(self.state):
                for member in team:
                    # Each member prefers to be assigned to a different team from past assignments.
                    if ti < len(past_teams) and member in past_teams[ti]:
                        v += DECAY_RATE**hi

                    # Different combinations of members are preferable.
                    other_members = team - {member}
                    past_team = self.find_team(member, past_teams)
                    if len(past_team) == 0:
                        continue
                    past_other_members = past_team - {member}
                    intersect = other_members & past_other_members
                    v += (DECAY_RATE**hi)*len(intersect)
        return v

    def find_team(self, member, teams):
        for team in teams:
            if member in team:
                return team
        return set()


def load_input(file_name):
    with open(file_name, 'r') as yml:
        config = yaml.safe_load(yml)

    load_settings(config['settings'])
    h = load_history(config['history'])
    p = load_preferences(config['preferences'])
    return h, p

def load_settings(input_settings):
    settings.num_members_in_each_team = input_settings['num_members_in_each_team']
    settings.num_remaining_members_in_each_team = input_settings['num_remaining_members_in_each_team']
    if len(settings.num_members_in_each_team) != len(settings.num_remaining_members_in_each_team):
        print("The number of elements in 'num_members_in_each_team' and 'num_remaining_members_in_each_team' must be the same.")
        sys.exit(1)
    settings.members = set(input_settings['members'])

    if sum(settings.num_members_in_each_team) != len(settings.members):
        print("invalid settings.")
        sys.exit(1)

def load_history(input_history):
    history = []
    for past_teams_list in input_history:
        tmp_past_teams = []
        for past_team_list in past_teams_list:
            tmp_past_team = set(past_team_list)
            tmp_past_teams.append(copy.copy(tmp_past_team))
        history.append(copy.deepcopy(tmp_past_teams))

    return history

def load_preferences(input_preferences):
    preferences = dict()
    for pref in input_preferences:
        name = pref['name']
        if name not in settings.members:
            print("preference for invalid member '{}' found.".format(name))
            sys.exit(1)
        class_anti_affinity = set()
        if 'class_anti_affinity' in pref:
            class_anti_affinity = set(pref['class_anti_affinity'])
        num_min_team_members = 0
        if 'num_min_team_members' in pref:
            num_min_team_members = pref['num_min_team_members']
        preferences[name] = Preference(class_anti_affinity, num_min_team_members)

    return preferences

def generate_initial_state():
    init_state = []
    tmp_members = copy.copy(settings.members)
    for num_members in settings.num_members_in_each_team:
        tmp_team = set()
        for i in range(num_members):
            tmp_team.add(tmp_members.pop())
        init_state.append(copy.copy(tmp_team))
    return init_state

def show_result(state):
    print()
    print()
    print("result:")
    for i, team in enumerate(state):
        print("team {}: {}".format(i, team))

def main():
    history, preferences = load_input(sys.argv[1])

    # initial assignment
    init_state = generate_initial_state()

    sh = SortingHat(init_state, preferences, history)
    sh.steps = 100000
    sh.copy_strategy = "deepcopy"
    sh.anneal()
    show_result(sh.state)

if __name__ == '__main__':
    main()
