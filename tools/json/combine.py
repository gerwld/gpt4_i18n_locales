import os
import json
from global_context import C_RED, C_GREEN

PATH_TO_JSONS_1 = 'dist/locales_copy/'
PATH_TO_JSONS_2 = 'dist/locales/'
PATH_TO_FINAL_RESULT = 'dist/locales_combined/'

# checks PATH_TO_RESULT_CHUNKS for non-existing translations
locale_files = os.listdir(PATH_TO_JSONS_1)
locale_files.remove(".DS_Store")
total_locales = len(locale_files)
print(f"{C_GREEN}Founded locales: {total_locales}{C_GREEN.OFF}")

# Create the output directory if it doesn't exist
os.makedirs(PATH_TO_FINAL_RESULT, exist_ok=True)

for i, locale in enumerate(locale_files, start=1):
    try:
        loc_path_1 = os.path.join(PATH_TO_JSONS_1, locale, "messages.json")
        loc_path_2 = os.path.join(PATH_TO_JSONS_2, locale, "messages.json")

        # Check if files exist
        if not os.path.exists(loc_path_1) or not os.path.exists(loc_path_2):
            raise FileNotFoundError

        # Load the json files
        with open(loc_path_1, 'r', encoding='utf-8') as file_1, open(loc_path_2, 'r', encoding='utf-8') as file_2:
            locale_content_1 = json.load(file_1)
            locale_content_2 = json.load(file_2)

            # Combine dictionaries using the | operator
            combined = locale_content_1 | locale_content_2

            # Create the locale output directory if it doesn't exist
            output_locale_dir = os.path.join(PATH_TO_FINAL_RESULT, locale)
            os.makedirs(output_locale_dir, exist_ok=True)

            # Save the modified translations back to the file
            output_path = os.path.join(output_locale_dir, "messages.json")
            with open(output_path, 'w', encoding='utf-8') as final_content:
                json.dump(combined, final_content, ensure_ascii=False, indent=2)

            print(f"{C_GREEN}[{i}/{total_locales}] Combined locale: {locale}{C_GREEN.OFF}, dest: {output_path}")

    except FileNotFoundError:
        print(f"{C_RED}[{i}/{total_locales}] Skipping locale {locale}: File missing{C_RED.OFF}")
    except json.JSONDecodeError:
        print(f"{C_RED}[{i}/{total_locales}] Skipping locale {locale}: JSON decoding error{C_RED.OFF}")
    except Exception as e:
        print(f"{C_RED}[{i}/{total_locales}] Skipping locale {locale}: {str(e)}{C_RED.OFF}")
