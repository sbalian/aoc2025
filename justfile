test:
    uv run ruff check .
    uv run pyright .
    uv run pytest

start:
    uv run good_morning.py

run day='':
    #!/usr/bin/env bash
    if [ -n "{{day}}" ]; then
        cd solutions/day{{day}} && uv run solution.py
    else
        for d in solutions/day*/; do
            echo "=== ${d%/} ==="
            (cd "$d" && uv run solution.py)
        done
    fi
