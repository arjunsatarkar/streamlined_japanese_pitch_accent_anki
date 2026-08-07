#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
import sqlite3
import csv

KANJIUM_SOURCE_PATH = "data/kanjium_accents.txt"


def main():
    kanjium_accents = {}

    # Kanjium - should be more reliable
    with open("data/kanjium_accents.txt") as f:
        kanjium_rows = csv.reader(f, delimiter="\t")
        for row in kanjium_rows:
            try:
                kanjium_accents[(row[0], row[1])] = int(row[2])
            except ValueError:
                # Can't parse if there are multiple accents but it's fine for now
                # That only applies to multi-word phrases
                continue

    conn = sqlite3.connect("data/pitch_accents.sqlite", autocommit=False)
    try:
        with conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS expression_reading_accent(
                    id INTEGER PRIMARY KEY,
                    expression TEXT,
                    reading TEXT,
                    accent INTEGER,
                    UNIQUE(expression, reading)
                ) STRICT;
            """)
            conn.executemany(
                "INSERT OR IGNORE INTO expression_reading_accent(expression, reading, accent) VALUES (?, ?, ?);",
                (
                    (expression, reading, accent)
                    for ((expression, reading), accent) in kanjium_accents.items()
                ),
            )
            conn.execute("ANALYZE;")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
