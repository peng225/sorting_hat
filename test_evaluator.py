import unittest
import input_handler
import evaluator

class TestEvaluator(unittest.TestCase):
    def setUp(self):
        pass

    def test_find_team(self):
        # No team exists.
        ev = evaluator.Evaluator({}, [], [])
        team = ev.find_team("m1", [])
        self.assertSetEqual(set(), team)

        # Three teams and member found.
        teams = [
            {"m1"}, {"m2", "m3"}, {"m4", "m5"}
        ]
        team = ev.find_team("m2", teams)
        self.assertSetEqual(teams[1], team)

        # Three teams and member not found.
        team = ev.find_team("m6", teams)
        self.assertSetEqual(set(), team)

    def test_evaluate_check_constraint(self):
        # Empty input.
        ev = evaluator.Evaluator({}, [], [])
        state = [
            {"m1"}, {"m2", "m3"}, {"m4", "m5"}
        ]
        v = ev.evaluate(state)
        self.assertEqual(0, sum(v))

        # class_anti_affinity is set and it is not violated.
        preferences = {"m2": input_handler.Preference({0, 2}, 0)}
        ev = evaluator.Evaluator(preferences, [], [])
        v = ev.evaluate(state)
        self.assertEqual(0, sum(v))

        # class_anti_affinity is set and it is violated.
        preferences = {"m2": input_handler.Preference({1}, 0)}
        ev = evaluator.Evaluator(preferences, [], [])
        v = ev.evaluate(state)
        self.assertEqual(ev.LARGE_VALUE, v[0])

        # min_num_team_members is violated.
        preferences = {"m2": input_handler.Preference(set(), 3)}
        ev = evaluator.Evaluator(preferences, [], [])
        v = ev.evaluate(state)
        self.assertEqual(ev.LARGE_VALUE, v[0])

        # num_remaining_members_in_each_team is not violated.
        history = [
            [{"m2", "m4"}, {"m1", "m3", "m5"}],
            [{"m1", "m3"}, {"m2", "m4"}]]
        num_remaining_members_in_each_team = [0, 1, 0]
        ev = evaluator.Evaluator(
            {}, history, num_remaining_members_in_each_team)
        v = ev.evaluate(state)
        self.assertLess(sum(v), ev.LARGE_VALUE)

        # num_remaining_members_in_each_team is violated.
        num_remaining_members_in_each_team = [0, 2, 0]
        ev = evaluator.Evaluator(
            {}, history, num_remaining_members_in_each_team)
        v = ev.evaluate(state)
        self.assertGreater(sum(v), ev.LARGE_VALUE)

    def test_evaluate_check_history_check(self):
        # One history with the same number of teams.
        # All members changes their teams and combinations.
        state = [
            {"m1"}, {"m2", "m3"}, {"m4", "m5"}
        ]
        history = [
            [{"m2", "m4"}, {"m1", "m5"}, {"m3"}]]
        num_remaining_members_in_each_team = [0, 0, 0]
        ev = evaluator.Evaluator(
            {}, history, num_remaining_members_in_each_team)
        v = ev.evaluate(state)
        self.assertEqual(0, sum(v))

        # One history with the same number of teams.
        # All members changes their combinations,
        # but "m2" does not change his/her team.
        history = [
            [{"m4"}, {"m2", "m5"}, {"m1", "m3"}]]
        num_remaining_members_in_each_team = [0, 0, 0]
        ev = evaluator.Evaluator(
            {}, history, num_remaining_members_in_each_team)
        v = ev.evaluate(state)
        self.assertAlmostEqual(1.0, v[1])

        # One history with the same number of teams.
        # All members changes their teams,
        # but "m2" and "m3" belongs to the same team again.
        history = [
            [{"m4"}, {"m1", "m5"}, {"m2", "m3"}]]
        num_remaining_members_in_each_team = [0, 0, 0]
        ev = evaluator.Evaluator(
            {}, history, num_remaining_members_in_each_team)
        v = ev.evaluate(state)
        self.assertAlmostEqual(1.0, v[2])

        # One history with the different number of teams.
        # "m4" and "m5" were in the same team which no longer exists.
        history = [
            [{"m3"}, {"m1", "m6"}, {"m2"}, {"m4", "m5"}]]
        num_remaining_members_in_each_team = [0, 0, 0]
        ev = evaluator.Evaluator(
            {}, history, num_remaining_members_in_each_team)
        v = ev.evaluate(state)
        self.assertAlmostEqual(1.0, v[2])

        # One history with the same number of teams.
        # A new member is added.
        history = [
            [{"m3"}, {"m1"}, {"m2"}]]
        num_remaining_members_in_each_team = [0, 0, 0]
        ev = evaluator.Evaluator(
            {}, history, num_remaining_members_in_each_team)
        v = ev.evaluate(state)
        self.assertEqual(0, sum(v))

        # Two histories with the same number of teams.
        history = [
            [{"m2", "m4"}, {"m1", "m5"}, {"m3"}],
            [{"m1"}, {"m4"}, {"m2", "m3"}]]
        num_remaining_members_in_each_team = [0, 0, 0]
        ev = evaluator.Evaluator(
            {}, history, num_remaining_members_in_each_team)
        v = ev.evaluate(state)
        self.assertAlmostEqual(1.0 * ev.DECAY_RATE, v[1])
        self.assertAlmostEqual(1.0 * ev.DECAY_RATE, v[2])
