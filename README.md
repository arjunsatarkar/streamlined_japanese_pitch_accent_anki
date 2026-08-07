# Streamlined Japanese Pitch Accent Add-On for Anki

A better [Anki](https://apps.ankiweb.net/) add-on to automatically add pitch accent information to a chosen field in Japanese vocabulary cards.

There are several of these already at time of creation, but they have some problems:

1. Overly complicated/busy pitch display. For Standard Japanese pitch accent, there is no need for a pitch graph. You only need to see the accented mora, or that there are none if the word is 平板型 (flat).
2. Use of questionable data (eg. Wadoku). At time of writing, many common words including 赤い have the wrong pitch pattern in this database.
3. Inability to parse Anki's built in square bracket based furigana notation (some note types don't have the reading in a separate field).

We address these as follows:

1. This add-on simply highlights the accented mora, eg. the accent of 柊 displays as <strong style="text-decoration: underline;">ひ</strong>いらぎ. Flat words display in italics so you don't have to hunt for an accented mora if there aren't any.
2. The AnkiWeb version of this add-on currently uses the [Kanjium accent data](https://github.com/mifunetoshiro/kanjium/blob/master/data/source_files/raw/accents.txt). This data also has some problems, such as ambiguity in what accent data with commas represents, but we have responded by not including any ambiguous cases. As far as we know, the data which *is* unambiguously parseable is generally correct and the best available. Open an issue if you can suggest better or supplementary accent data!
3. This add-on can parse square bracket furigana notation *or* get the reading from a separate field.

## Install

See https://ankiweb.net/shared/info/678172946.

## Copying

Streamlined Japanese Pitch Accent

© 2026-present [Arjun Satarkar](https://arjunsatarkar.net/) &lt;me@arjunsatarkar.net&gt;

This program is free software: you can redistribute it and/or modify it under the terms of
the GNU Affero General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

See `LICENSE.txt` in the repository root for the text of the license.

## Acknowledgements

Although we have not included any code from previous add-ons, we have benefited from the concept of and inspiration from [IllDepence/anki_add_pitch_plugin](https://github.com/IllDepence/anki_add_pitch_plugin).
