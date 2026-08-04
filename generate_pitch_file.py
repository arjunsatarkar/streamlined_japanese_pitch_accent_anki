#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
import sqlite3
import xml.etree.ElementTree as ET
import sys


def main():
    conn = sqlite3.connect("data/pitch_accents.sqlite", autocommit=False)
    ns = {"entry": "http://www.wadoku.de/xml/entry"}
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    try:
        with conn:
            conn.executescript("""
                CREATE TABLE expression_reading_accent(
                    id INTEGER PRIMARY KEY,
                    expression TEXT,
                    reading TEXT,
                    accent INTEGER,
                    UNIQUE(expression, reading)
                ) STRICT;
            """)
            for entry in root:
                orths = [orth.text for orth in entry.findall("entry:form/entry:orth", ns)]
                assert orths
                reading = entry.find("entry:form/entry:reading/entry:hira", ns).text
                try:
                    accent = int(
                        entry.find("entry:form/entry:reading/entry:accent", ns).text
                    )
                except (AttributeError, ValueError):
                    # We can't parse complex pitch patterns for multi-word phrases where there are multiple
                    # drops, but that's fine, it's out of scope.
                    continue
                conn.executemany(
                    "INSERT OR IGNORE INTO expression_reading_accent(expression, reading, accent) VALUES (?, ?, ?);",
                    ((orth, reading, accent) for orth in orths),
                )
            conn.execute("ANALYZE;")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
