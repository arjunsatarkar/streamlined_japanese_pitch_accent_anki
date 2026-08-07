build: copy_db_to_addon_folder
    rm -f streamlined_japanese_pitch_accent.ankiaddon
    cd addon && zip -r ../streamlined_japanese_pitch_accent.ankiaddon * -x '__pycache__/*'

copy_db_to_addon_folder:
    cp data/pitch_accents.sqlite addon/
