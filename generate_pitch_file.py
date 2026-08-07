#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
import sqlite3
import xml.etree.ElementTree as ET
import sys
import csv

KANJIUM_SOURCE_PATH = "data/kanjium_accents.txt"
WADOKU_SOURCE_PATH = "data/wadoku-xml-20260705/wadoku.xml"

def main():
    kanjium_accents = {}
    wadoku_accents = {}

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

    # Wadoku - less reliable
    ns = {"entry": "http://www.wadoku.de/xml/entry"}
    tree = ET.parse(WADOKU_SOURCE_PATH)
    root = tree.getroot()
    for entry in root:
        orths = [orth.text for orth in entry.findall("entry:form/entry:orth", ns)]
        assert orths
        reading = entry.find("entry:form/entry:reading/entry:hira", ns).text
        try:
            accent = int(
                entry.find("entry:form/entry:reading/entry:accent", ns).text
            )
        except (AttributeError, ValueError):
            # Same as earlier with multi-word phrases
            # Also if there is no accent in Wadoku for the word
            continue
        for orth in orths:
            wadoku_accents[(orth, reading)] = accent


    sys.stderr.write(f"Kanjium: {len(kanjium_accents)}. Wadoku: {len(wadoku_accents)}")

    with open("data/discrepancies.tsv", "w") as f:
        f.write("expression\treading\taccent_kanjium\taccent_wadoku\n")
        for key in kanjium_accents:
            accent_kanjium = kanjium_accents[key]
            try:
                accent_wadoku = wadoku_accents[key]
            except KeyError:
                continue
            if accent_wadoku != accent_kanjium:
                f.write(f"{key[0]}\t{key[1]}\t{accent_kanjium}\t{accent_wadoku}\n")

    """
    conn = sqlite3.connect("data/pitch_accents.sqlite", autocommit=False)
    try:
        with conn:
            conn.executescript(\"""
                CREATE TABLE expression_reading_accent(
                    id INTEGER PRIMARY KEY,
                    expression TEXT,
                    reading TEXT,
                    accent INTEGER,
                    UNIQUE(expression, reading)
                ) STRICT;
            \""")
            conn.executemany(
                "INSERT OR IGNORE INTO expression_reading_accent(expression, reading, accent) VALUES (?, ?, ?);",
                ((orth, reading, accent) for orth in orths),
            )
            conn.execute("ANALYZE;")
    finally:
        conn.close()
    """
        
if __name__ == "__main__":
    main()
