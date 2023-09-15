class Evaluator:
    LARGE_VALUE = 10000
    DECAY_RATE = 0.9
    diff_team_prefer_rate: float
    preferences = {}
    history = []
    num_remaining_members_in_each_team = []

    def __init__(self, preferences, history,num_remaining_members_in_each_team,
                 diff_team_prefer_rate = 1.0):
        self.preferences = preferences
        self.history = history
        self.num_remaining_members_in_each_team = num_remaining_members_in_each_team
        self.diff_team_prefer_rate = diff_team_prefer_rate

    def evaluate(self, state):
        v = 0.0
        # Check constraints.
        # When a constraint is violated, a very large value is added to the energy.
        for ti, team in enumerate(state):
            for member in team:
                if member not in self.preferences:
                    continue
                if ti in self.preferences[member].class_anti_affinity:
                    v += self.LARGE_VALUE
                if len(team) < self.preferences[member].num_min_team_members:
                    v += self.LARGE_VALUE

            if len(self.history) == 0 or len(self.history) <= ti:
                continue

            prev_team = self.history[0][ti]
            if len(team & prev_team) < self.num_remaining_members_in_each_team[ti]:
                v += self.LARGE_VALUE

        # Check preferable conditions.
        for hi, past_teams in enumerate(self.history):
            for ti, team in enumerate(state):
                for member in team:
                    # Each member prefers to be assigned to a different team from past assignments.
                    if ti < len(past_teams) and member in past_teams[ti]:
                        v += self.diff_team_prefer_rate * self.DECAY_RATE**hi

                    # Different combinations of members are preferable.
                    other_members = team - {member}
                    past_team = self.find_team(member, past_teams)
                    if len(past_team) == 0:
                        continue
                    past_other_members = past_team - {member}
                    intersect = other_members & past_other_members
                    # To eliminate the double count for each member per one combination,
                    # the added value is divided by 2.0.
                    v += (self.DECAY_RATE**hi)*len(intersect) / 2.0
        return v

    def find_team(self, member, teams):
        for team in teams:
            if member in team:
                return team
        return set()
