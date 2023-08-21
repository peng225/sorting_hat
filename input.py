import yaml
import sys
import copy

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

def load(file_name):
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
