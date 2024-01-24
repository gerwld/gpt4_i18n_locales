import json
from global_context import C_RED


# перевіряє чи пост відповідає заданим критеріям. якщо ні - повертає False
def isLocaleValid(original_locale, translated_locale):
    if not original_locale:
      print(f"{C_RED}isLocaleValid: message.json is corrupted or missing{C_RED.OFF}")
    if not translated_locale:
      print(f"{C_RED}isLocaleValid: translated_locale is corrupted or missing{C_RED.OFF}")

    # звірка кількості ключів і { }
    if translated_locale and str(translated_locale):
      try:
        t_keys = list(json.loads(translated_locale).keys())
        orig_keys = list(json.loads(original_locale).keys())
        print(f"{C_RED}Translated json keys: {len(t_keys)}, original: {len(orig_keys)}{C_RED.OFF}")
        
        if len(t_keys) == len(orig_keys) and str(translated_locale).strip() != str(original_locale).strip() and translated_locale[0] == "{" and translated_locale[-1] == "}":
            return True;
      except:
         return False
      
    return False
