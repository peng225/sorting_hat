import copy
import evaluator
import input_handler

class BruteForceAssigner():
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
        self.best_scores = [(float('inf'), float('inf'), float('inf'))
                            for i in range(self.num_results)]
        self.state = [set() for i in range(len(self.settings.num_members_in_each_team))]
        current_num_members_in_each_team = copy.copy(self.settings.num_members_in_each_team)
        current_members = copy.copy(self.settings.members)
        self.search_helper(current_num_members_in_each_team, current_members)

    def search_helper(self, current_num_members_in_each_team, current_members):
        if sum(current_num_members_in_each_team) == 0:
            assert len(
                current_members) == 0, f"len(current_members) == {len(current_members)}"
            v = self.ev.evaluate(self.state)
            for i, bs in enumerate(self.best_scores):
                if sum(v) < sum(bs):
                    self.best_states = self.best_states[:i] + \
                        [copy.deepcopy(self.state)] + self.best_states[i:-1]
                    self.best_scores = self.best_scores[:i] + \
                        [v] + self.best_scores[i:-1]
                    break
            return

        tmp_member = current_members.pop()
        for i, _ in enumerate(current_num_members_in_each_team):
            if current_num_members_in_each_team[i] == 0:
                continue
            current_num_members_in_each_team[i] -= 1
            self.state[i].add(tmp_member)
            self.search_helper(current_num_members_in_each_team, current_members)
            self.state[i].remove(tmp_member)
            current_num_members_in_each_team[i] += 1
        current_members.add(tmp_member)

    def show_result(self):
        print("result:")
        for i, bs in enumerate(self.best_scores):
            print(f"order: {i}")
            print(f"value: {sum(bs)} {bs}")
            for j, team in enumerate(self.best_states[i]):
                print(f"team {j}: {team}")
            print("")
