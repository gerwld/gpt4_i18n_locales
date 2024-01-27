import json
from global_context import C_RED

MIN_LENGTH_DESC = 500
SHOULD_BE_IN_DESC = ["##", "1.1.4", "example.com"]
FIRST_STR_DESC_SHOULD_CONTAIN = ":"
FIRST_STR_DESC_SHOULD_CONTAIN_OR = "："
LAST_STR_DESC_SHOULD_CONTAIN = "..."

def all_strings_present(strings_list, main_string):
    return all(string in main_string for string in strings_list)

# перевіряє чи пост відповідає заданим критеріям. якщо ні - повертає False
def isDescriptionValid(description):
    description = str(description)
    if not description:
      print(f"{C_RED}isDescriptionValid: translated_description is corrupted or missing{C_RED.OFF}")

    # if description req. length is true, then
    if len(str(description)) > MIN_LENGTH_DESC:
      # and all string present
      if  all_strings_present(SHOULD_BE_IN_DESC, description):
        # and first contain (chineese : or regular ascii)
        if FIRST_STR_DESC_SHOULD_CONTAIN  in description.split('\n')[0] or FIRST_STR_DESC_SHOULD_CONTAIN_OR in description.split('\n')[0]:
          # and last contain
          if LAST_STR_DESC_SHOULD_CONTAIN in description.split('\n')[-1]:
           return True;
      
    return False
