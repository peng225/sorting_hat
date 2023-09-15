#!/usr/bin/python3

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
    args = parser.parse_args()

    # parse YAML input
    state_yaml = yaml.safe_load(args.raw_state)
    state = []
    for sy in state_yaml["state"]:
        state.append(set(sy))

    print(f"state: {state}")
    settings, preferences, history = input_handler.load(args.filename)
    ev = evaluator.Evaluator(preferences, history,
                             settings.num_remaining_members_in_each_team)

    v = ev.evaluate(state)
    print(f"value: {v}")

if __name__ == '__main__':
    main()
