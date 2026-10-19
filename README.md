# Graham Scan — Convex Hull

## Overview

This project implements the **Graham Scan algorithm**, a computational geometry algorithm used to compute the convex hull of a set of points in a two-dimensional plane.

The convex hull is the smallest convex polygon that contains all the given points.

## Features

- Computes the convex hull of a set of 2D points.
- Uses geometric operations to determine the orientation of points.
- Identifies the points that form the boundary of the convex hull.
- Demonstrates a fundamental algorithm in computational geometry.

## Algorithm

The Graham Scan algorithm works in the following steps:

1. Find the point with the lowest vertical coordinate.
2. Sort the remaining points by their polar angle relative to that point.
3. Process the sorted points using a stack.
4. Remove points that would create a clockwise turn or violate the convex boundary.
5. The remaining points form the convex hull.

## Technologies

- **Programming language:** Add your language here (C++, Python, Java, etc.)
- **Version control:** Git
- **Repository hosting:** GitHub

## Getting Started

### Clone the repository

```bash
git clone https://github.com/YOUBY-25/graham_hull_project.git
```

### Navigate to the project directory

```bash
cd graham_hull_project
```

### Run the program

Use the appropriate command for your programming language.

For example, for C++:

```bash
g++ main.cpp -o graham_hull
./graham_hull
```

For Python:

```bash
python main.py
```

*Adjust the filenames and commands to match the actual project files.*

## Complexity Analysis

- **Time complexity:** \(O(n \log n)\), mainly due to sorting the points.
- **Space complexity:** \(O(n)\) for storing the points and the convex hull stack.

Here, \(n\) is the number of input points.

## Applications

- Computational geometry
- Computer graphics
- Geographic information systems (GIS)
- Collision detection
- Shape analysis

## Author

Ayoub

## License

This project was created for educational purposes as part of a Computational Geometry laboratory assignment.
