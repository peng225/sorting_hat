import unittest
import sorting_hat

class TestSortingHat(unittest.TestCase):
    def setUp(self):
        sorting_hat.settings = sorting_hat.Settings()
    
    def test_load_settings(self):
        input_settings = dict()
        input_settings['num_members_in_each_team'] = [1, 2, 3]
        input_settings['num_remaining_members_in_each_team'] = [0, 0, 0]
        input_settings['members'] = ["m1", "m2", "m3", "m4", "m5", "m6"]

        sorting_hat.load_settings(input_settings)

        for v in input_settings['num_members_in_each_team']:
            self.assertTrue(v in sorting_hat.settings.num_members_in_each_team)
        for v in input_settings['num_remaining_members_in_each_team']:
            self.assertTrue(v in sorting_hat.settings.num_remaining_members_in_each_team)
        for v in input_settings['members']:
            self.assertTrue(v in sorting_hat.settings.members)

    def test_load_history(self):
        # Empty history
        input_history = []
        output_history = sorting_hat.load_history(input_history)
        self.assertEqual(0, len(output_history))

        # Two histories in the same form
        input_history = [
            [["m1", "m2"], ["m3"], ["m4", "m5"]],
            [["m1", "m3"], ["m4"], ["m2", "m5"]],
        ]
        output_history = sorting_hat.load_history(input_history)
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
        output_history = sorting_hat.load_history(input_history)
        self.assertEqual(2, len(output_history))
        self.assertEqual(2, len(output_history[0][0]))
        self.assertEqual(1, len(output_history[0][1]))
        self.assertEqual(2, len(output_history[0][2]))
        self.assertEqual(2, len(output_history[1][0]))
        self.assertEqual(2, len(output_history[1][1]))
        self.assertEqual(1, len(output_history[1][2]))

if __name__ == '__main__':
    unittest.main()
