from aqt import gui_hooks
from aqt import mw
from aqt.browser import Browser
from aqt.qt import *
from aqt.utils import chooseList, getText, showInfo, showText, qconnect
import aqt.operations.note
import os

from . import utils


def about() -> None:
    showText(
        """
    <h1>Streamlined Japanese Pitch Accent</h1>
    © 2026-present <a href="https://arjunsatarkar.net/">Arjun Satarkar</a> &lt;me@arjunsatarkar.net&gt;<br>
    <i>See license information below.</i>

    <h2>How To Use</h2>
    <p>To add or remove pitch accents, select all cards you want to change in the card browser and use the context menu.</p>
    <p>
        For more info or to report issues, see the
        <a href="https://github.com/arjunsatarkar/streamlined_japanese_pitch_accent_anki">source code repository</a>.
    </p>

    <h2 id="license_info">License Information</h2>
    <p>
        This program is free software: you can redistribute it and/or modify it under the terms of
        the GNU Affero General Public License as published by the Free Software Foundation, version 3.
    </p>
    <p>
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU Affero General Public License for more details.
    </p>
    """,
        title="Streamlined Japanese Pitch Accent",
        type="html",
    )


def add_pitch_accent(browser: Browser) -> None:
    notes = [mw.col.get_note(note_id) for note_id in browser.selected_notes()]
    if len(set(note.mid for note in notes)) != 1:
        showInfo(
            "Can only add pitch accent to one note type at a time; select cards of the same note type"
        )
        return
    field_names = [field["name"] for field in notes[0].note_type()["flds"]]
    jp_exp_index = chooseList(
        "Where is the Japanese expression?", field_names, parent=browser
    )
    reading_index = (
        chooseList(
            "Where is the reading?",
            [
                "❕ It is Anki-style (square-bracket []) furigana alongside the expression itself"
            ]
            + field_names,
            parent=browser,
        )
        - 1
    )
    pitch_accent_index = chooseList(
        "Where should the pitch accent go? (The note will be skipped if this field is not empty.)",
        field_names,
        parent=browser,
    )

    conn = utils.get_conn()
    added = 0
    skipped_not_found = 0
    skipped_field_not_empty = 0
    try:
        for note in notes:
            if reading_index == -1:
                expression, reading = utils.parse_furigana(
                    note[field_names[jp_exp_index]]
                )
            else:
                expression = note[field_names[jp_exp_index]]
                reading = note[field_names[reading_index]]
            db_reading = "" if expression == reading else reading
            result = conn.execute(
                "SELECT accent FROM expression_reading_accent WHERE expression = ? AND reading = ?;",
                (expression, db_reading),
            ).fetchone()
            if result:
                accented_mora: int = result[0]
            else:
                skipped_not_found += 1
                continue
            if note[field_names[pitch_accent_index]] != "":
                skipped_field_not_empty += 1
                continue
            note[field_names[pitch_accent_index]] = utils.render_accent(
                reading, accented_mora
            )
            added += 1

        aqt.operations.note.update_notes(parent=browser, notes=notes).success(
            lambda _: showInfo(
                f"Added accents to {added} notes, skipped {skipped_not_found} because the expression-reading"
                f" combination was not found and {skipped_field_not_empty} because the field was not empty"
                f" (skipped {skipped_not_found + skipped_field_not_empty} in total)."
            )
        ).run_in_background()
    finally:
        conn.close()


def add_manual_pitch_accent(browser: Browser) -> None:
    notes = [mw.col.get_note(note_id) for note_id in browser.selected_notes()]
    if len(notes) > 1:
        showInfo(
            "Can only manually add pitch accent info to one note at a time; select just one."
        )
        return
    note = notes[0]
    reading, _ = getText("Enter the reading in kana.")
    if not reading:
        showInfo("Reading not provided; doing nothing for now.")
        return
    accented_mora, _ = getText("Enter the number of the accented mora (0 for heiban).")
    try:
        accented_mora = int(accented_mora)
        if accented_mora < 0:
            raise ValueError
    except ValueError:
        showInfo(
            "The accented mora should be a positive integer number; doing nothing for now."
        )
        return
    field_names = [field["name"] for field in note.note_type()["flds"]]
    pitch_accent_index = chooseList(
        "Where should the pitch accent go? (In manual mode, this field will be overwritten if not empty!)",
        field_names,
    )
    note[field_names[pitch_accent_index]] = utils.render_accent(
        reading, accented_mora, auto_added=False
    )
    aqt.operations.note.update_note(parent=browser, note=note).run_in_background()


def remove_pitch_accent(browser: Browser) -> None:
    notes = [mw.col.get_note(note_id) for note_id in browser.selected_notes()]
    if len(set(note.mid for note in notes)) != 1:
        showInfo(
            "Can only remove pitch accent from one note type at a time; select cards of the same note type"
        )
        return
    field_names = [field["name"] for field in notes[0].note_type()["flds"]]
    pitch_accent_index = chooseList(
        "Which field to remove pitch accent from? (This will only affect fields populated automatically by this add-on.)",
        field_names,
        parent=browser,
    )

    removed_from = 0
    skipped = 0
    for note in notes:
        if utils.is_field_populated_by_this_addon(
            note[field_names[pitch_accent_index]]
        ):
            note[field_names[pitch_accent_index]] = ""
            removed_from += 1
        else:
            skipped += 1
    aqt.operations.note.update_notes(parent=browser, notes=notes).success(
        lambda _: showInfo(
            f"Removed accents from {removed_from} notes, skipped {skipped} notes."
        )
    ).run_in_background()


def on_browser_will_show_context_menu(browser: Browser, menu: QMenu) -> None:
    submenu = QMenu("Streamlined JP Pitch Accent", browser)
    add_action = submenu.addAction("Add Pitch Accent")
    remove_action = submenu.addAction("Remove Pitch Accent")
    add_manual_action = submenu.addAction("Set Pitch Accent Manually")

    qconnect(add_action.triggered, lambda: add_pitch_accent(browser))
    qconnect(remove_action.triggered, lambda: remove_pitch_accent(browser))
    qconnect(add_manual_action.triggered, lambda: add_manual_pitch_accent(browser))

    menu.addMenu(submenu)


topbar_menu = QMenu("Streamlined JP Pitch Accent", mw)
help_about_license_action = topbar_menu.addAction("Help/About/License")
qconnect(help_about_license_action.triggered, about)
mw.form.menuTools.addMenu(topbar_menu)

gui_hooks.browser_will_show_context_menu.append(on_browser_will_show_context_menu)
