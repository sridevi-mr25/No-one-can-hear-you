# No One Can Hear You: Path Planning Through a Spreading Fire

A fire breaks out on a spaceship and spreads every turn. A bot has to reach the exit before the fire reaches the bot. This project compares four planning strategies, from "plan once and hope" to an adaptive planner that prices fire risk into every step.

*Rutgers CS520 (Intro to AI), part 1 of 3. Part 2 is [Space-Rats](https://github.com/sridevi-mr25/Space-Rats) and part 3 is [Bot-Localization](https://github.com/sridevi-mr25/Bot-Localization).*

## The environment

- **The ship** is a 40 × 40 maze generated at random. Dead ends are partly opened up so there are several routes.
- **The fire** starts in a random open cell. Each turn, an open cell catches fire with probability `1 − (1 − q)^k`, where `k` is the number of burning neighbours and `q` is the ship's flammability (0 to 1).
- **The bot** moves one cell per turn. It succeeds if it reaches the exit and fails if the fire reaches its cell first.

## The four bots

| Bot | Strategy |
|---|---|
| **Bot 1** | Plans the shortest path once with A* and follows it, ignoring the fire. |
| **Bot 2** | Replans with A* every turn, avoiding cells that are currently on fire. |
| **Bot 3** | Replans every turn, avoiding fire and cells next to fire. If no safe path exists, it relaxes and allows fire-adjacent cells. |
| **Bot 4** | Adaptive A* with a fire-risk cost. Each cell's cost includes its chance of catching fire, weighted more heavily as flammability rises. Heuristics are updated between searches. |

## Findings

Bot 4, the risk-aware planner, outperformed plain and repeated A*. Its advantage was largest at high flammability, where the shortest path is often the most dangerous one.

## How to run

```bash
pip install numpy matplotlib

python Bot1final.py    # or Bot2final.py, Bot3final.py, Bot4final.py
```

Each run creates a new random ship, fire position and flammability `q`. It prints the start and goal, then plots the grid at every step. **Close each plot window to advance one step.**

## Repository contents

| File | Contents |
|---|---|
| `grid.py` | Maze generation and choice of start and goal |
| `fire1.py` | Fire placement, spread model and fire-adjacency checks |
| `algorithm.py` | A* search shared by Bots 1–3 |
| `Bot1final.py` … `Bot4final.py` | The four bots |
| `plot.py` | Grid visualization |
| `constants.py` | Grid size and cell types |
