from anki.models import NotetypeId
from aqt import mw
from enum import Enum, auto


class FieldPurpose(Enum):
    JAPANESE_EXPRESSION = auto()
    READING = auto()
    PITCH_ACCENT = auto()


class Config:
    def __init__(self):
        self.config = mw.addonManager.getConfig(__name__)

    def get_last_used_field_idx(
        self,
        note_type_id: NotetypeId,
        field_purpose: FieldPurpose,
        field_names: list[str],
    ) -> int:
        try:
            return field_names.index(
                self.config["note_type_default_field_names"][str(note_type_id)][
                    field_purpose.name
                ]
            )
        except (KeyError, ValueError):
            if field_purpose is FieldPurpose.READING:
                return -1
            return 0

    def set_last_used_field_name(
        self, note_type_id: NotetypeId, field_purpose: FieldPurpose, field_name: str
    ) -> None:
        self.config["note_type_default_field_names"].setdefault(str(note_type_id), {})[
            field_purpose.name
        ] = field_name
        mw.addonManager.writeConfig(__name__, self.config)

    def clear_last_used_field_name(
        self, note_type_id: NotetypeId, field_purpose: FieldPurpose
    ) -> None:
        self.config["note_type_default_field_names"].setdefault(str(note_type_id), {})[
            field_purpose.name
        ] = None
        mw.addonManager.writeConfig(__name__, self.config)
