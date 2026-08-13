import pathlib
import sqlite3
import unicodedata

# See https://en.wikipedia.org/wiki/Tag_URI_scheme. (Global uniqueness.)
PITCH_ACCENT_FIELD_START = (
    "<!--tag:arjunsatarkar.net,2026:streamlined_japanese_pitch_accent_auto_added-->"
)
PITCH_ACCENT_FIELD_END = PITCH_ACCENT_FIELD_START


def get_conn() -> sqlite3.Connection:
    return sqlite3.connect(
        pathlib.Path(__file__).parent / "pitch_accents.sqlite", autocommit=False
    )


def parse_furigana(s: str):
    expression = ""
    reading = ""
    in_html_tag = False
    in_furigana = False
    current_segment_ambiguous_chars = ""
    for c in s:
        if c == "<":
            in_html_tag = True
            continue
        if c == ">":
            in_html_tag = False
            continue
        if in_html_tag:
            continue
        if c == " ":
            expression += current_segment_ambiguous_chars
            reading += current_segment_ambiguous_chars
            current_segment_ambiguous_chars = ""
            continue
        if c == "[":
            in_furigana = True
            expression += current_segment_ambiguous_chars
            current_segment_ambiguous_chars = ""
            continue
        if c == "]":
            in_furigana = False
            continue
        if in_furigana:
            reading += c
            continue
        current_segment_ambiguous_chars += c
    expression += current_segment_ambiguous_chars
    reading += current_segment_ambiguous_chars

    return expression, reading


def is_field_populated_by_this_addon(s: str) -> bool:
    return s.startswith(PITCH_ACCENT_FIELD_START) and s.endswith(PITCH_ACCENT_FIELD_END)


def render_accent(reading: str, accented_mora: int, auto_added: bool = True) -> str:
    result = ""
    reading = unicodedata.normalize("NFC", reading)
    if accented_mora != 0:
        MORAIC_CHARACTERS = set(
            unicodedata.normalize(
                "NFC",
                "あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばひびふぶへべほぼまみむめもやゆよらりるれろわをんっ"
                "アイウエオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂツヅテデトドナニヌネノハバヒビフブヘベホボマミムメモヤユヨラリルレロワヲンッー",
            )
        )
        current_mora = 0
        in_accented_mora = False
        for char in reading:
            if char in MORAIC_CHARACTERS:
                current_mora += 1
            if current_mora == accented_mora:
                if not in_accented_mora:
                    result += '<strong style="text-decoration: underline;">'
                    in_accented_mora = True
            elif in_accented_mora:
                result += "</strong>"
                in_accented_mora = False
            result += char
        # Close the tag if the last mora was accented
        if in_accented_mora:
            result += "</strong>"
    else:
        result = f"<span style='text-decoration: overline;'>{reading}</span>"
    if auto_added:
        result = f"{PITCH_ACCENT_FIELD_START}{result}{PITCH_ACCENT_FIELD_END}"
    return result
