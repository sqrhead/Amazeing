 *This project has been created as part of the 42 curriculum by fshelna and rarriola.*

---

# A-Maze-ing 🌀

## Description

A-Maze-ing is a Python maze generator and visualizer. Given a configuration file, it generates a randomized maze using the **Recursive Backtracker** (depth-first search) algorithm, optionally ensures it is a *perfect maze* (exactly one path between any two cells), displays it in the terminal with ASCII art, and writes the result — including the shortest path — to a hexadecimal output file.

Key features:
- Deterministic generation via a user-defined seed
- Perfect and imperfect maze modes
- Embedded **"42" pattern** carved into the center of the maze
- BFS-based shortest path solver
- Interactive terminal menu: regenerate, show/hide path, rotate wall colors
- Hexadecimal output file with entry, exit, and directional path

---

## Instructions

### Requirements

- Python 3.10 or later
- `flake8` and `mypy` for linting (see Makefile)

### Installation

```bash
make install
```

### Run

```bash
make run
# or directly:
python3 a_maze_ing.py config.txt
```

The program takes exactly one argument: the path to a configuration file.

```bash
python3 a_maze_ing.py my_config.txt
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint          # flake8 + mypy standard
make lint-strict   # flake8 + mypy --strict
```

### Clean

```bash
make clean
```

---

## Configuration File Format

The config file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are ignored as comments. Spaces around `=` and values are accepted.

| Key           | Type    | Required | Description                              | Example               |
|---------------|---------|----------|------------------------------------------|-----------------------|
| `WIDTH`       | int     | ✅        | Number of cells horizontally (≥ 5, ≤ 100000) | `WIDTH=20`        |
| `HEIGHT`      | int     | ✅        | Number of cells vertically (≥ 5, ≤ 100000)   | `HEIGHT=15`       |
| `ENTRY`       | x,y     | ✅        | Entry cell coordinates (inside bounds)   | `ENTRY=0,0`           |
| `EXIT`        | x,y     | ✅        | Exit cell coordinates (≠ ENTRY, in bounds) | `EXIT=19,14`        |
| `OUTPUT_FILE` | string  | ✅        | Output filename, must end in `.txt`      | `OUTPUT_FILE=maze.txt`|
| `PERFECT`     | bool    | ✅        | `true` = one unique path; `false` = loops allowed | `PERFECT=true` |
| `SEED`        | int     | ❌        | Random seed for reproducibility (≥ 1). If omitted, a random seed is used. | `SEED=42` |

Example `config.txt`:
```
# A-Maze-ing config
WIDTH  = 10
HEIGHT = 10
ENTRY  = 1, 5
EXIT   = 5, 5
OUTPUT_FILE = myoutput.txt
PERFECT = true
SEED = 1998
```

---

## Output File Format

The output file is structured as follows:

```
<hex grid, one row per line>
<empty line>
<entry_x>,<entry_y>
<exit_x>,<exit_y>
<shortest path as N/E/S/W characters>
```

Each cell is encoded as a single hexadecimal digit where each bit represents a closed wall:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1       | East  |
| 2       | South |
| 3       | West  |

A bit set to `1` means the wall is **closed**; `0` means **open**.

Example: `A` (binary `1010`) = East and West walls are closed.

If no path exists between entry and exit, the path line contains `no path`.

---

## Maze Generation Algorithm

The project uses the **Recursive Backtracker** algorithm, also known as depth-first search maze generation.

### How it works

1. Start from a random cell and mark it as visited.
2. While there are unvisited cells on the stack:
   - Pick a random unvisited neighbor.
   - Remove the wall between the current cell and that neighbor.
   - Push the neighbor onto the stack and mark it visited.
   - If no unvisited neighbors exist, pop the stack (backtrack).
3. Border walls are explicitly restored after generation.
4. In **imperfect mode**, a post-processing step randomly removes additional interior walls to create loops.

### Why this algorithm?

- **Simple to implement** from scratch using an explicit stack (no recursion limit issues).
- **Produces long, winding corridors** — mazes that feel organic and challenging.
- **Guaranteed full connectivity** — every cell is reachable from any other (perfect maze = spanning tree).
- **Fast** — O(n) time and space for n cells.
- Straightforward to extend with an imperfect mode by selectively removing extra walls.

---

## Pathfinding

The `Pathfinder` class uses **Breadth-First Search (BFS)** to find the shortest path between entry and exit. It traces back through `PathfinderNode` parent references to reconstruct the exact path.

---

## Code Reusability

### The `MazeGenerator` class (`mazegen.py`)

`MazeGenerator` is a standalone, importable module that can be reused in any future project.

**Installation (from built package):**
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

**Basic usage:**
```python
from mazegen import MazeGenerator

# Create a 20x15 maze with seed 42, entry at (0,0), exit at (19,14)
gen = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42)

# Generate a perfect maze (one unique path between any two cells)
grid = gen.generate(perfect=True)

# grid is a list[list[int]] — each int encodes walls as bits:
# bit0=North, bit1=East, bit2=South, bit3=West (1=closed, 0=open)
print(grid[0][0])  # e.g. 9 = 1001 = North+West walls closed

# Access the "42" pattern cell positions
print(gen.pattern_cells)  # list of (x, y) tuples

# Find the shortest path using the included Pathfinder
from pathfinder import Pathfinder
pf = Pathfinder(grid)
path = pf.get_path((0, 0), (19, 14))
# path is a list of (x, y) tuples from entry to exit
print(path)
```

**Custom parameters:**
```python
# Imperfect maze (contains loops)
grid = gen.generate(perfect=False)

# Without seed (random each time)
gen = MazeGenerator(width=30, height=30, entry=(0, 0), exit=(29, 29), seed=None)
```

**Accessed structure:**
- `gen.grid` — `list[list[int]]` — the raw cell data after generation
- `gen.pattern_cells` — `list[tuple[int, int]]` — coordinates of the "42" symbol cells
- `gen.width`, `gen.height` — dimensions

**Building the package:**
```bash
pip install build
python -m build
# Produces dist/mazegen-1.0.0-py3-none-any.whl and dist/mazegen-1.0.0.tar.gz
```

---

## Team & Project Management

### Team

This project was completed in team by **fshelna and rarriola**.

### Planning

| Phase | Planned | Actual |
|-------|---------|--------|
| Maze generation algorithm | Day 1–2 | Day 1–2 |
| Hex output file + parser | Day 2–3 | Day 3 |
| Pathfinder (BFS) | Day 3 | Day 3–4 |
| Terminal displayer | Day 4 | Day 4–5 |
| Config parser + error handling | Day 4 | Day 5 |
| Cleanup, docstrings, linting | Day 5 | Day 6 |

The displayer took longer than expected due to the double-cell ASCII rendering and handling the "42" pattern as special tiles.

### What worked well

- The Recursive Backtracker algorithm was clean to implement with an explicit stack.
- BFS pathfinding integrated naturally with the same grid structure.
- Separating each concern into its own class (generator, pathfinder, displayer, filehex, parser) made debugging straightforward.

### What could be improved

- The `__init__.py` package structure needs to be finalized before building the pip-installable package.
- More edge case tests (very small mazes, entry/exit at every possible border position).
- The imperfect mode could be more controlled to guarantee no unreachable dead zones.

### Tools used

- **VSCode** with Python extension for development
- **flake8** and **mypy** for static analysis
- **Claude (Anthropic)** — used for reviewing error handling logic, suggesting docstring formats, and explaining BFS path reconstruction. All generated suggestions were reviewed, tested, and adapted manually.

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker explained — jamisbuck.org](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Breadth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python type hints — docs.python.org](https://docs.python.org/3/library/typing.html)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)

### AI usage

Claude (Anthropic) was used during this project for:
- Reviewing edge cases in the config parser error handling
- Suggesting the `PathfinderNode` parent-tracing pattern for BFS reconstruction
- Explaining PEP 257 docstring formatting conventions
- Reviewing flake8/mypy compliance issues

All AI-generated suggestions were read, understood, tested, and adapted before integration. No code was blindly copy-pasted.
