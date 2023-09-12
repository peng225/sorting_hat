#!/usr/bin/python3

import argparse
import evaluator
import input_handler
import annealing
import brute_force

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='FILE_NAME', type=str,
                        help='input file name')
    parser.add_argument('--algorithm', dest='algorithm', action='store',
                        type=str, default="brute_force",
                        help='search algorithm ("brute_force" or "annealing")')
    parser.add_argument('--steps', dest='steps', action='store',
                        type=int, default=10000,
                        help='(for annealing algorithm) the number of annealing steps')
    parser.add_argument('--max_temp', dest='tmax', action='store',
                        type=float, default=25000.0,
                        help='(for annealing algorithm) the maximum temperature of annealing')
    parser.add_argument('--top', dest='num_results', action='store',
                        type=int, default=1,
                        help='(for brute force algorithm) the number of results')
    args = parser.parse_args()

    settings, preferences, history = input_handler.load(args.filename)
    ev = evaluator.Evaluator(preferences, history,
                             settings.num_remaining_members_in_each_team)

    if args.algorithm == "brute_force":
        bfa = brute_force.BruteForceAssigner(ev, settings, args.num_results)
        bfa.search()
        bfa.show_result()
    elif args.algorithm == "annealing":
        init_state = annealing.generate_initial_state(settings)
        ana = annealing.AnnealingAssigner(init_state, ev, settings)
        ana.steps = args.steps
        ana.Tmax = args.tmax
        ana.copy_strategy = "deepcopy"
        ana.anneal()
        ana.show_result()
    else:
        print(f"invalid algorithm: {args.algorithm}")

if __name__ == '__main__':
    main()
