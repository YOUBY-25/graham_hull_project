"""
Laboratory Work No. 6 — Convex Hulls: Graham's Scan
Python 3.8+

Run:
    python main.py                 # Task 1 + visualization
    python main.py --trace         # print stack changes for a small example
    python main.py --experiment    # benchmark n = 100, 1000, 5000, 10000
    python main.py --all           # run all tasks

The implementation is written for this lab; it does not use a built-in
convex-hull function.
"""

from dataclasses import dataclass
from math import atan2
from random import Random
from statistics import mean
from time import perf_counter
import argparse
from typing import Iterable, List, Sequence, Tuple


@dataclass(frozen=True, order=True)
class Point:
    """A point in the two-dimensional plane."""
    x: float
    y: float


def cross(a: Point, b: Point, c: Point) -> float:
    """Return the signed cross product; positive means a left turn."""
    return ((b.x - a.x) * (c.y - a.y)
            - (b.y - a.y) * (c.x - a.x))


def dist2(a: Point, b: Point) -> float:
    """Squared Euclidean distance (avoids an unnecessary square root)."""
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


def unique_points(points: Iterable[Point]) -> List[Point]:
    """Remove duplicate coordinates while keeping deterministic ordering."""
    return sorted(set(points), key=lambda p: (p.x, p.y))


def graham_hull(points: Iterable[Point], trace: bool = False) -> List[Point]:
    """
    Construct the convex hull in counterclockwise order using Graham's scan.

    The start point has minimum y; ties are broken by choosing maximum x.
    Collinear points along a ray from the start are reduced to the farthest
    point, so only extreme vertices are returned. Duplicate points are ignored.
    """
    pts = unique_points(points)
    if len(pts) <= 1:
        return pts
    if len(pts) == 2:
        return [min(pts, key=lambda p: (p.y, -p.x)),
                max(pts, key=lambda p: (p.y, -p.x))]

    p0 = min(pts, key=lambda p: (p.y, -p.x))
    others = [p for p in pts if p != p0]
    others.sort(key=lambda p: (
        atan2(p.y - p0.y, p.x - p0.x),
        dist2(p0, p)
    ))

    # Points at the same polar angle lie on the same ray. Keep only the
    # farthest one, which is the only one that can be a hull vertex.
    filtered: List[Point] = []
    for p in others:
        while filtered and cross(p0, filtered[-1], p) == 0:
            if dist2(p0, p) >= dist2(p0, filtered[-1]):
                removed = filtered.pop()
                if trace:
                    print(f"Same-angle filtering: removed {removed}")
            else:
                break
        if not filtered or cross(p0, filtered[-1], p) != 0:
            filtered.append(p)

    # If all points are collinear, the filtered list has only the far endpoint.
    if len(filtered) == 1:
        return [p0, filtered[0]]

    hull: List[Point] = [p0, filtered[0]]
    if trace:
        print(f"Initial stack: {hull}")

    for p in filtered[1:]:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            removed = hull.pop()
            if trace:
                print(f"Adding {p}: removed {removed} (non-left turn)")
                print(f"  stack now: {hull}")
        hull.append(p)
        if trace:
            print(f"Added {p}: stack = {hull}")

    return hull


def plot_hull(points: Iterable[Point], hull: Sequence[Point]) -> None:
    """Plot input points and the closed convex hull polygon."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            "Visualization requires matplotlib. Install it with: "
            "python -m pip install matplotlib"
        ) from exc

    pts = list(points)
    plt.figure(figsize=(7, 7))
    if pts:
        plt.scatter([p.x for p in pts], [p.y for p in pts],
                    label="Original points")
    if len(hull) >= 2:
        closed = list(hull) + [hull[0]]
        plt.plot([p.x for p in closed], [p.y for p in closed],
                 linewidth=2, marker="o", label="Convex hull")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Graham's Scan")
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def run_basic_task(show_plot: bool = True) -> Tuple[List[Point], List[Point]]:
    """Run Task 1 with the point set specified in the laboratory handout."""
    points = [
        Point(1, 0), Point(1, 1), Point(6, 1),
        Point(6, 3), Point(3, 2), Point(5, 3),
        Point(5, 6), Point(3, 4), Point(2, 4),
    ]
    hull = graham_hull(points)
    print("Task 1 — original points:")
    print(points)
    print("\nConvex hull vertices (counterclockwise order):")
    for i, point in enumerate(hull, start=1):
        print(f"{i}. {point}")
    if show_plot:
        plot_hull(points, hull)
    return points, hull


def run_stack_task() -> None:
    """Demonstrate stack changes on a small set of points."""
    points = [
        Point(0, 0), Point(2, 0), Point(3, 1), Point(2, 2),
        Point(1, 1), Point(0, 2), Point(1, 0.5), Point(2, 1),
        Point(1, 2), Point(3, 0),
    ]
    print("Task 2 — stack trace:")
    print("Input points:", points)
    hull = graham_hull(points, trace=True)
    print("\nFinal hull:", hull)


def test_special_cases() -> None:
    """Exercise duplicate, collinear, and same-angle cases."""
    cases = {
        "duplicate points": [
            Point(0, 0), Point(2, 0), Point(2, 0),
            Point(2, 2), Point(0, 2), Point(1, 1)
        ],
        "same polar angle / points on an edge": [
            Point(0, 0), Point(1, 1), Point(2, 2),
            Point(3, 3), Point(3, 0), Point(0, 3)
        ],
        "all points collinear": [
            Point(0, 0), Point(1, 1), Point(2, 2),
            Point(3, 3), Point(2, 2)
        ],
        "one point": [Point(4, 4)],
        "two points": [Point(0, 0), Point(1, 1)],
    }
    print("Task 3 — special cases:")
    for name, points in cases.items():
        print(f"{name}: {graham_hull(points)}")


def benchmark(sizes: Sequence[int] = (100, 1000, 5000, 10000),
              repeats: int = 10, seed: int = 2026) -> None:
    """Measure average hull construction time for reproducible random sets."""
    rng = Random(seed)
    print("\nTask 4 — experimental complexity")
    print(f"{'n':>8} | {'average (s)':>14} | {'minimum (s)':>14}")
    print("-" * 43)
    for n in sizes:
        points = [Point(rng.random() * 10000, rng.random() * 10000)
                  for _ in range(n)]
        timings = []
        for _ in range(repeats):
            start = perf_counter()
            graham_hull(points)
            timings.append(perf_counter() - start)
        print(f"{n:8d} | {mean(timings):14.6f} | {min(timings):14.6f}")
    print("Note: timings depend on hardware and system load.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Graham's scan convex hull lab")
    parser.add_argument("--trace", action="store_true",
                        help="show stack operations for a small point set")
    parser.add_argument("--experiment", action="store_true",
                        help="run timing experiment for several input sizes")
    parser.add_argument("--all", action="store_true",
                        help="run basic task, stack trace, special cases and benchmark")
    parser.add_argument("--no-plot", action="store_true",
                        help="do not display the Task 1 plot")
    args = parser.parse_args()

    run_basic_task(show_plot=not args.no_plot and not args.trace
                   and not args.experiment and not args.all)
    if args.trace or args.all:
        run_stack_task()
    if args.all:
        test_special_cases()
    if args.experiment or args.all:
        benchmark()


if __name__ == "__main__":
    main()
