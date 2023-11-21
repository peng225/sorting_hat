from dataclasses import dataclass
import sys
import copy
import yaml


@dataclass
class Settings:
    min_num_members_in_each_team = []
    max_num_members_in_each_team = []
    num_remaining_members_in_each_team = []
    members = set()

    def __init__(
        self,
        min_num_members_in_each_team,
        max_num_members_in_each_team,
        num_remaining_members_in_each_team,
        members,
    ):
        self.min_num_members_in_each_team = min_num_members_in_each_team
        self.max_num_members_in_each_team = max_num_members_in_each_team
        self.num_remaining_members_in_each_team = num_remaining_members_in_each_team
        self.members = members


@dataclass
class Preference:
    class_anti_affinity = set()
    min_num_team_members = 0

    def __init__(self, class_anti_affinity, min_num_team_members):
        self.class_anti_affinity = class_anti_affinity
        self.min_num_team_members = min_num_team_members


def load(file_name):
    with open(file_name, "r", encoding="utf-8") as yml:
        config = yaml.safe_load(yml)

    s = load_settings(config["settings"])
    if s is None:
        sys.exit(1)
    p = load_preferences(
        config["preferences"], s.members, len(s.min_num_members_in_each_team)
    )
    h = load_history(config["history"])
    if p is None:
        sys.exit(1)
    return s, p, h


def load_settings(input_settings):
    settings = Settings(
        input_settings["min_num_members_in_each_team"],
        input_settings["max_num_members_in_each_team"],
        input_settings["num_remaining_members_in_each_team"],
        set(input_settings["members"]),
    )

    if (
        len(settings.min_num_members_in_each_team)
        != len(settings.max_num_members_in_each_team)
    ) or (
        len(settings.min_num_members_in_each_team)
        != len(settings.num_remaining_members_in_each_team)
    ):
        print(
            "The number of elements in 'min_num_members_in_each_team', \
'max_num_members_in_each_team' and \
'num_remaining_members_in_each_team' must be the same."
        )
        return None
    if len(settings.min_num_members_in_each_team) < 2:
        print("The number of teams must be larger than or equal to 2.")
        return None
    if len(settings.members) < sum(settings.min_num_members_in_each_team):
        print(
            f"The number of members is too small. \
(settings.min_num_members_in_each_team = {settings.min_num_members_in_each_team}, \
len(settings.members) = {len(settings.members)})"
        )
        return None
    if sum(settings.max_num_members_in_each_team) < len(settings.members):
        print(
            f"The number of members is too large. \
(settings.max_num_members_in_each_team = {settings.max_num_members_in_each_team}, \
len(settings.members) = {len(settings.members)})"
        )
        return None
    for i, _ in enumerate(settings.max_num_members_in_each_team):
        if (
            settings.max_num_members_in_each_team[i]
            < settings.num_remaining_members_in_each_team[i]
        ):
            print(
                f"Each element of 'max_num_members_in_each_team' must be larger than or \
equal to the corresponding element of 'num_remaining_members_in_each_team'. \
(i = {i}, settings.max_num_members_in_each_team[i] = {settings.max_num_members_in_each_team[i]}, \
settings.num_remaining_members_in_each_team[i] = {settings.num_remaining_members_in_each_team[i]})"
            )
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
    preferences = {}
    for pref in input_preferences:
        name = pref["name"]
        if name not in members:
            print(f"preference for invalid member '{name}' found.")
            return None
        class_anti_affinity = set()
        if "class_anti_affinity" in pref:
            class_anti_affinity = set(pref["class_anti_affinity"])
            for caa in class_anti_affinity:
                if num_teams <= caa:
                    print(
                        "Each value of 'class_anti_affinity' \
                          must be less than the number of teams."
                    )
                    return None
        min_num_team_members = 0
        if "min_num_team_members" in pref:
            min_num_team_members = pref["min_num_team_members"]
        preferences[name] = Preference(class_anti_affinity, min_num_team_members)

    return preferences
