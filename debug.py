#!/usr/bin/python3

import sys
import argparse
import yaml
import evaluator
import input_handler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='FILE_NAME', type=str,
                        help='input file name')
    parser.add_argument('--state', dest='raw_state', action='store',
                        type=str, default="", required=True,
                        help='state to be checked in YAML format \
                            (e.g. {"state": [["hayato", "taro", "masao"], ["kenta", "saburo"], \
                                ["takashi", "jiro", "takuya"]]})')
    parser.add_argument('--diff_team_prefer_rate', dest='diff_team_prefer_rate', action='store',
                        type=float, default=1.0,
                        help='(advanced option) see implementation of evaluator')
    args = parser.parse_args()

    if args.diff_team_prefer_rate < 0:
        print(
            f"invalid value of diff_team_prefer_rate: {args.diff_team_prefer_rate}")
        sys.exit(1)

    # parse YAML input
    state_yaml = yaml.safe_load(args.raw_state)
    state = []
    for sy in state_yaml["state"]:
        state.append(set(sy))

    print(f"state: {state}")
    settings, preferences, history = input_handler.load(args.filename)
    ev = evaluator.Evaluator(preferences, history,
                             settings.num_remaining_members_in_each_team,
                             args.diff_team_prefer_rate)

    v = ev.evaluate(state)
    print(f"value: {sum(v)} {v}")

if __name__ == '__main__':
    main()
