import os
import json
from global_context import C_RED, C_GREEN

PATH_TO_JSONS = 'dist/locales_copy/'
PATH_TO_FINAL_RESULT = 'dist/locales_copy/'
KEYS_TO_REMOVE = ['mi_2', 'mi_3', 'mi_6', 'mi_14', 'mi_15', 'mi_16', 'themes_msg', 'themes_msg', 'themes_msg', 'themes_msg']

# checks PATH_TO_RESULT_CHUNKS for non-existing translations
locale_files = os.listdir(PATH_TO_JSONS) 
locale_files.remove(".DS_Store")
total_locales = len(locale_files)
print(f"{C_GREEN}Founded locales: {total_locales}{C_GREEN.OFF}")

for i, locale in enumerate(locale_files, start=1):
    try:
        loc_path = os.path.join(f"{PATH_TO_JSONS}{locale}", "messages.json")

        # Load the existing translations
        with open(loc_path, 'r', encoding='utf-8') as locale_content:
            translations = json.load(locale_content)

        # Remove unused keys
        for key in KEYS_TO_REMOVE:
            if key in translations:
                del translations[key]

        # Save the modified translations back to the file
        with open(loc_path, 'w', encoding='utf-8') as locale_content:
            json.dump(translations, locale_content, ensure_ascii=False, indent=2)

        print(f"{C_GREEN}[{i}/{total_locales}] Removed unused keys for locale {locale}{C_GREEN.OFF}")

    except FileNotFoundError:
        print(f"{C_RED}[{i}/{total_locales}] Skipping locale {locale}: File missing{C_RED.OFF}")
    except json.JSONDecodeError:
        print(f"{C_RED}[{i}/{total_locales}] Skipping locale {locale}: JSON decoding error{C_RED.OFF}")
