import yaml
import sys
import copy

class Settings:
    num_members_in_each_team = []
    num_remaining_members_in_each_team = []
    members = set()

class Preference:
    class_anti_affinity = set()
    num_min_team_members = 0

    def __init__(self, class_anti_affinity, num_min_team_members):
        self.class_anti_affinity = class_anti_affinity
        self.num_min_team_members = num_min_team_members

def load(file_name):
    with open(file_name, 'r') as yml:
        config = yaml.safe_load(yml)

    s = load_settings(config['settings'])
    if s == None:
        sys.exit(1)
    h = load_history(config['history'])
    p = load_preferences(config['preferences'], s.members, len(s.num_members_in_each_team))
    if p == None:
        sys.exit(1)
    return s, h, p

def load_settings(input_settings):
    settings = Settings()
    settings.num_members_in_each_team = input_settings['num_members_in_each_team']
    settings.num_remaining_members_in_each_team = input_settings['num_remaining_members_in_each_team']
    if len(settings.num_members_in_each_team) != len(settings.num_remaining_members_in_each_team):
        print("The number of elements in 'num_members_in_each_team' and 'num_remaining_members_in_each_team' must be the same.")
        return None
    if len(settings.num_members_in_each_team) < 2:
        print("The number of teams must be larger than or equal to 2.")
        return None

    settings.members = set(input_settings['members'])
    if len(settings.members) <= 1:
        print("The number of members should be larger than 1.")
        return None
    if sum(settings.num_members_in_each_team) != len(settings.members):
        print("Invalid settings. (settings.num_members_in_each_team = {}, len(settings.members) = {})".format(
            settings.num_members_in_each_team,
            len(settings.members)))
        return None

    return settings

def load_history(input_history):
    history = []
    for past_teams_list in input_history:
        tmp_past_teams = []
        for past_team_list in past_teams_list:
            tmp_past_team = set(past_team_list)
            tmp_past_teams.append(copy.copy(tmp_past_team))
        history.append(copy.deepcopy(tmp_past_teams))

    return history

def load_preferences(input_preferences, members, num_teams):
    preferences = dict()
    for pref in input_preferences:
        name = pref['name']
        if name not in members:
            print("preference for invalid member '{}' found.".format(name))
            return None
        class_anti_affinity = set()
        if 'class_anti_affinity' in pref:
            class_anti_affinity = set(pref['class_anti_affinity'])
            for caa in class_anti_affinity:
                if num_teams <= caa:
                    print("Each value of 'class_anti_affinity' must be less than the number of teams.")
                    return None
        num_min_team_members = 0
        if 'num_min_team_members' in pref:
            num_min_team_members = pref['num_min_team_members']
        preferences[name] = Preference(class_anti_affinity, num_min_team_members)

    return preferences
