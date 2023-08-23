import unittest
import input_handler

class TestInputHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_settings(self):
        input_settings = {}
        input_settings['num_members_in_each_team'] = [1, 2, 3]
        input_settings['num_remaining_members_in_each_team'] = [0, 0, 0]
        input_settings['members'] = ["m1", "m2", "m3", "m4", "m5", "m6"]

        settings = input_handler.load_settings(input_settings)

        for v in input_settings['num_members_in_each_team']:
            self.assertTrue(v in settings.num_members_in_each_team)
        for v in input_settings['num_remaining_members_in_each_team']:
            self.assertTrue(v in settings.num_remaining_members_in_each_team)
        for v in input_settings['members']:
            self.assertTrue(v in settings.members)

    def test_load_history(self):
        # Empty history
        input_history = []
        output_history = input_handler.load_history(input_history)
        self.assertEqual(0, len(output_history))

        # Two histories in the same form
        input_history = [
            [["m1", "m2"], ["m3"], ["m4", "m5"]],
            [["m1", "m3"], ["m4"], ["m2", "m5"]],
        ]
        output_history = input_handler.load_history(input_history)
        self.assertEqual(2, len(output_history))
        self.assertEqual(2, len(output_history[0][0]))
        self.assertEqual(1, len(output_history[0][1]))
        self.assertEqual(2, len(output_history[0][2]))
        self.assertEqual(2, len(output_history[1][0]))
        self.assertEqual(1, len(output_history[1][1]))
        self.assertEqual(2, len(output_history[1][2]))

        # Two histories in the different forms
        input_history = [
            [["m1", "m2"], ["m3"], ["m4", "m5"]],
            [["m1", "m3"], ["m2", "m4"], ["m5"]],
        ]
        output_history = input_handler.load_history(input_history)
        self.assertEqual(2, len(output_history))
        self.assertEqual(2, len(output_history[0][0]))
        self.assertEqual(1, len(output_history[0][1]))
        self.assertEqual(2, len(output_history[0][2]))
        self.assertEqual(2, len(output_history[1][0]))
        self.assertEqual(2, len(output_history[1][1]))
        self.assertEqual(1, len(output_history[1][2]))

    def test_load_preferences(self):
        # Empty preference
        input_preferences = {}
        output_preferences = input_handler.load_preferences(input_preferences, [], 3)
        self.assertEqual(0, len(output_preferences))

        # Two preferences
        input_preferences = [
            {'name': 'ryu', 'num_min_team_members': 1},
            {'name': 'ken', 'num_min_team_members': 2, 'class_anti_affinity': {0, 2}}
        ]
        members =['ryu', 'ken']
        output_preferences = input_handler.load_preferences(input_preferences, members, 3)
        self.assertEqual(2, len(output_preferences))
        self.assertEqual(1, output_preferences['ryu'].num_min_team_members)
        self.assertEqual(2, output_preferences['ken'].num_min_team_members)
        self.assertEqual({0, 2}, output_preferences['ken'].class_anti_affinity)

if __name__ == '__main__':
    unittest.main()
