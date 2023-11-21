#!/usr/bin/python3

import sys
import argparse
import evaluator
import input_handler
import brute_force


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", metavar="FILE_NAME", type=str, help="input file name"
    )
    parser.add_argument(
        "--top",
        dest="num_results",
        action="store",
        type=int,
        default=1,
        help="the number of results (> 0)",
    )
    parser.add_argument(
        "--diff_team_prefer_rate",
        dest="diff_team_prefer_rate",
        action="store",
        type=float,
        default=1.0,
        help="(advanced option) see implementation of evaluator",
    )
    args = parser.parse_args()

    if args.num_results <= 0:
        print(f"invalid value of num_results: {args.num_results}")
        sys.exit(1)
    if args.diff_team_prefer_rate < 0:
        print(f"invalid value of diff_team_prefer_rate: {args.diff_team_prefer_rate}")
        sys.exit(1)

    settings, preferences, history = input_handler.load(args.filename)
    ev = evaluator.Evaluator(
        preferences,
        history,
        settings.num_remaining_members_in_each_team,
        args.diff_team_prefer_rate,
    )

    bfa = brute_force.BruteForceAssigner(ev, settings, args.num_results)
    bfa.search()
    bfa.show_result()


if __name__ == "__main__":
    main()
