import copy
import evaluator
import input_handler


class BruteForceAssigner:
    ev: evaluator.Evaluator
    settings: input_handler.Settings
    num_results: int
    state = []
    best_states = []
    best_scores = []

    def __init__(self, ev, settings, num_result):
        self.ev = ev
        self.settings = settings
        self.num_results = num_result

    def search(self):
        self.best_states = [[] for i in range(self.num_results)]
        self.best_scores = [
            (float("inf"), float("inf"), float("inf")) for i in range(self.num_results)
        ]
        num_teams = len(self.settings.min_num_members_in_each_team)
        self.state = [set() for i in range(num_teams)]
        num_assigned_members = [0 for i in range(num_teams)]
        to_be_assigned_members = copy.copy(self.settings.members)
        self.search_helper(num_assigned_members, to_be_assigned_members)

    def search_helper(self, num_assigned_members, to_be_assigned_members):
        if len(to_be_assigned_members) == 0:
            for i, n in enumerate(num_assigned_members):
                if n < self.settings.min_num_members_in_each_team[i]:
                    return
            v = self.ev.evaluate(self.state)
            for i, bs in enumerate(self.best_scores):
                if sum(v) < sum(bs):
                    self.best_states = (
                        self.best_states[:i]
                        + [copy.deepcopy(self.state)]
                        + self.best_states[i:-1]
                    )
                    self.best_scores = (
                        self.best_scores[:i] + [v] + self.best_scores[i:-1]
                    )
                    break
            return

        tmp_member = to_be_assigned_members.pop()
        for i, _ in enumerate(num_assigned_members):
            if num_assigned_members[i] == self.settings.max_num_members_in_each_team[i]:
                continue
            num_assigned_members[i] += 1
            self.state[i].add(tmp_member)
            self.search_helper(num_assigned_members, to_be_assigned_members)
            self.state[i].remove(tmp_member)
            num_assigned_members[i] -= 1
        to_be_assigned_members.add(tmp_member)

    def show_result(self):
        print("result:")
        for i, bs in enumerate(self.best_scores):
            print(f"order: {i}")
            print(f"value: {sum(bs)} {bs}")
            for j, team in enumerate(self.best_states[i]):
                print(f"team {j}: {team}")
            print("")
