#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
import csv
import itertools
import sqlite3

KANJIUM_SOURCE_PATH = "data/kanjium_accents.txt"


def main():
    accents = {}

    with open("data/kanjium_accents.txt") as kanjium_file:
        with open("data/extra_data.tsv") as extra_file:
            rows = itertools.chain(csv.reader(kanjium_file, delimiter="\t"), csv.reader(extra_file, delimiter="\t"))
            for row in rows:
                try:
                    accents[(row[0], row[1])] = int(row[2])
                except ValueError:
                    # Can't parse if there are multiple accents (unavoidable)
                    # In the kanjium data it's ambiguous whether those are multiple accepted
                    # variants, or a phrase with multiple accent patterns.
                    # See https://github.com/mifunetoshiro/kanjium/issues/14
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
                    for ((expression, reading), accent) in accents.items()
                ),
            )
            conn.execute("ANALYZE;")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
