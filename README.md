# Boruvka's Algorithm

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test](https://github.com/IsaacCheng9/boruvkas-algorithm/actions/workflows/test.yml/badge.svg)](https://github.com/IsaacCheng9/boruvkas-algorithm/actions/workflows/test.yml)

An implementation of Boruvka's algorithm to find a minimum spanning tree in a graph.

[Link to narrated video demonstration on YouTube.](https://www.youtube.com/watch?v=n5LNVobuBNU)

## Example
<img width="481" alt="image" src="https://github.com/IsaacCheng9/boruvkas-algorithm/assets/47993930/70c6d09e-7273-4416-8194-f4fe37701ef2">

<details>
  <summary>stdout (Terminal Output)</summary>
  
```
Finding MST with Boruvka's algorithm:
Vertices: [0, 1, 2, 3, 4, 5, 6, 7, 8]
Edges (node1, node2, weight):
    (0, 1, 4)
    (0, 6, 7)
    (1, 2, 9)
    (1, 6, 11)
    (1, 7, 20)
    (2, 3, 6)
    (2, 4, 2)
    (3, 4, 10)
    (3, 5, 5)
    (4, 5, 15)
    (4, 7, 1)
    (4, 8, 5)
    (5, 8, 12)
    (6, 7, 1)
    (7, 8, 3)

Iteration 1:
Current MST edges: []
Current MST Weight: 0
Added edge 0 - 1 with weight 4 to MST.
Added edge 2 - 4 with weight 2 to MST.
Added edge 3 - 5 with weight 5 to MST.
Added edge 4 - 7 with weight 1 to MST.
Added edge 6 - 7 with weight 1 to MST.
Added edge 7 - 8 with weight 3 to MST.

Iteration 2:
Current MST edges: [(0, 1, 4), (2, 4, 2), (3, 5, 5), (4, 7, 1), (6, 7, 1), (7, 8, 3)]
Current MST Weight: 16
Added edge 0 - 6 with weight 7 to MST.
Added edge 2 - 3 with weight 6 to MST.

MST found with Boruvka's algorithm.
MST edges (node1, node2, weight):
    (0, 1, 4)
    (0, 6, 7)
    (2, 3, 6)
    (2, 4, 2)
    (3, 5, 5)
    (4, 7, 1)
    (6, 7, 1)
    (7, 8, 3)
MST weight: 29
```
</details>

## Usage

### Installing Dependencies

Run the following command from the [project root](./) directory:

```bash
poetry install
```

### Running the Application

Run the following command from the [project root](./) directory:

```bash
poetry run app
```

### Running Tests

Run the following command from the [project root](./) directory:

```bash
poetry run pytest
```
