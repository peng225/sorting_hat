# Sorting Hat

Sorting Hat is a tool, inspired by [this blog post](https://qiita.com/matsulib/items/bd50af2e2bc1e48522cd), to decide the team assignment of people.

## What kind of problem does Sorting Hat solve?

Consider the situation where there are several persons and teams. Each person is assigned to one team, and the team assignment is periodically changed. Then, suppose we have to decide on the next team assignment. Sorting Hat finds a good assignment under the following conditions:

- People want to be assigned to a different team as possible.
  - But a few members may have to stay in the same team.
- People want to be on a team with different people every time they change teams.
- Some people may want to avoid specific teams.
- Some people may not want to be assigned to a too-small team.


## Install dependencies

```sh
python -m pip install --upgrade pip
pip install simanneal
pip install pyyaml
```

## Algorithms

There are two algorithms to solve the team assignment problem: the brute force search and the simulated annealing. The algorithm can be specified by `--algorithm` option (default = `brute_force`).

## Input file format

Input file is in the YAML format. The detailed format is as follows. See also the [sample_input.yaml](./sample_input.yaml).

- settings
  - num_members_in_each_team
    - type: list of integers
    - required: true
    - description: The number of members in each team. The values in the list must be ordered by team ID.
  - num_remaining_members_in_each_team
    - type: list of integers
    - required: true
    - description: The number of members who should remain in the same team. The values in the list must be ordered by team ID.
  - members:
    - type: list of strings
    - required: true
    - description: The name of each member.
- history
  - type: list of lists of strings
  - required: false
  - description: The history of team assignment. The values in the list must be in chronological order. The latest history must come first.
- preferences
  - type: list of the tuple of the following values
  - required: false
    - name
      - type: string
      - required: true (when preferences are used)
      - description: The name of the member to whom the setting is applied.
    - num_min_team_members
      - type: integer
      - required: false
      - description: The minimum number of members in the assigned team.
    - class_anti_affinity
      - type: list of integers
      - required: false
      - description: The list of class IDs to which the member must not be assigned.
