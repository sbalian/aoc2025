test:
    uv run ruff check .
    uv run basedpyright .
    uv run pytest

start:
    uv run good_morning.py

run day:
    cd solutions/day{{day}} && uv run solution.py
