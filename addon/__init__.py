from aqt import mw
from aqt.utils import showText, qconnect
from aqt.qt import *


def about() -> None:
    showText(
        """
    <h1>Streamlined Japanese Pitch Accent</h1>
    © 2026-present <a href="https://arjunsatarkar.net/">Arjun Satarkar</a> &lt;me@arjunsatarkar.net&gt; + contributors<br>
    <i>See license information below</i>

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


menu = QMenu("Streamlined JP Pitch Accent", mw)
help_about_license_action = menu.addAction("Help/About/License")
qconnect(help_about_license_action.triggered, about)

mw.form.menuTools.addMenu(menu)
