# Laboratory Work No. 6 — Graham's Scan

A Python 3.8+ implementation of Graham's algorithm for constructing a convex hull.

## Files
- `main.py` — geometric predicates, Graham scan, plotting, stack trace, special-case checks, and timing experiment.
- `requirements.txt` — optional plotting dependency.

## Setup
```bash
python -m pip install -r requirements.txt
```

## Run
```bash
python main.py
python main.py --trace
python main.py --experiment
python main.py --all
```

Use `python main.py --no-plot` to run Task 1 without opening a plot window.

## Notes
- The starting point has the smallest y-coordinate; ties choose the rightmost point.
- The hull is returned in counterclockwise order.
- Duplicate coordinates are removed.
- Collinear points on the same ray from the start are reduced to the farthest point; a fully collinear input returns its two extreme endpoints.
- Expected time complexity is `O(n log n)`: sorting takes `O(n log n)` and the stack pass is `O(n)`.
- Benchmark values are machine-dependent and are printed by the experiment rather than hard-coded in the report.
