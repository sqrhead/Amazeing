# Amazeing
Phase 1: Environment & Standards

    [ ] Project Skeleton: Setup .gitignore, Makefile, and virtual environment.

    [ ] Linting: Configure flake8 and mypy for strict type checking (Python 3.10+).

    [V] Config Parser: Handle KEY=VALUE input and error management.

Phase 2: The Core (mazegen module)

    [V] Generation Algorithm: Implement the Recursive   tracker (Depth-First Search).

    [V] The "42" Easter Egg: Logic to carve a "42" shape using closed cells.

    [ ] The Solver: Shortest path calculation (BFS/DFS) outputted as N, E, S, W strings.

    [ ] Data Export: Generate the Hexadecimal grid where bits represent walls.

Phase 3: Visualization & Interaction

    [V] Display: Terminal ASCII rendering or MiniLibX interface.

    [ ] User Controls: Implement keys for re-generation, toggling the solution path, and color rotation.

Phase 4: Delivery

    [ ] Packaging: Create a mazegen-*.whl or .tar.gz for pip installation.

    [ ] Final Review: Ensure all functions use try-except and context managers.

Configuration File Format

The configuration file must use the following structure:

    WIDTH / HEIGHT: Dimensions of the maze (in cells).

    ENTRY / EXIT: Coordinates (x,y) for start and finish.

    OUTPUT_FILE: Path to save the hex representation.

    PERFECT: Boolean (True/False) for unique path generation.

Algorithm Choice

    Chosen Algorithm: Recursive Backtracker (DFS).

    Why: It creates long, complex corridors which are visually interesting and guarantees a "Perfect" maze (spanning tree) with zero isolated cells.

Reusable Module

The logic is contained within the MazeGenerator class inside the mazegen package. You can install it using pip install ./mazegen-1.0.0-py3-none-any.whl.
Resources & AI Use

    Graph Theory: Prim's and Kruskal's algorithm references.

    AI Usage: AI was used for [mention tasks here, e.g., "designing the bitwise conversion logic and brainstorming the UI interactions"]. All AI-generated code was reviewed, tested, and typed manually.

Project Management

    Roles: Single contributor.

    Tools: uv for dependency management, pytest for unit testing.

Would you like me to help you draft the Makefile next so you can start with a clean environment?