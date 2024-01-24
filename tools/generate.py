"""Entry-point, translates every locale from languages.txt based on the reference (messages.json)"""
import os
import time
import json
import random

from tools.handlers.gptHandler import ChatGPTHandler
from tools.validators.isLocaleValid import isLocaleValid
from tools.handlers.auth import GPT_AUTH
from global_context import PATH_TO_RESULT, C_GREEN, C_RED, C_BLUE, PRODUCT_NAME

import chromedriver_autoinstaller
try:
    chromedriver_autoinstaller.install()
except Exception as e:
    print(f"{C_RED}Error during ChromeDriver update: {e}{C_RED.OFF}")

MESSAGE_PART1 = 'Translate to '
MESSAGE_PART2 = f'. Answer only with result in ```:\n'

while True: 
    with open("languages.txt", "r") as file:
        languages = file.read().splitlines()
        localesList = [item.split(":")[0] for item in languages]
        print('-'*90 + f'\n{C_GREEN}GPT4_locales start. Languages.txt total: {len(localesList)}{C_GREEN.OFF}')

        # checks PATH_TO_RESULT for non-existing translations
        completed = []
        try: 
            completed = os.listdir(PATH_TO_RESULT) 
        except: pass
        todoLangList = [i for i in localesList if i not in completed]
        print('-'*90 + f'\n{C_BLUE}To-do: {len(todoLangList)}. {C_BLUE.OFF}{C_GREEN}Completed locales in {PATH_TO_RESULT}:{C_GREEN.OFF} {len(completed)} {f"({completed})" if len(completed) else ""}')

        # if not all translations were created, then read messages.json and translate not translated yet
        if len(todoLangList) > 0:
            with open("messages.json", "r") as file:
                originalLocale = file.read()

                chatgpt = ChatGPTHandler(*GPT_AUTH, strip_first_3 = True)
                for lang in todoLangList:
                    currentLangName = [mask for mask in languages if mask.startswith(lang)][0].split(":")[1]
                    delay = random.randint(1, 4)
                    print(f'{C_GREEN}Working with: {lang}...{C_GREEN.OFF}')
                    gptRequest = f"{MESSAGE_PART1}{currentLangName} ({lang}){MESSAGE_PART2}{originalLocale}"
                    answer = chatgpt.interact(gptRequest)

                    # if response is valid, then create PATH_TO_RESULT/lang/message.json with response
                    if isLocaleValid(str(originalLocale), str(answer)):
                        try:                    
                            if not os.path.exists(f"{PATH_TO_RESULT}{lang}"):
                                os.makedirs(f"{PATH_TO_RESULT}{lang}")
                            file_path = os.path.join(f"{PATH_TO_RESULT}{lang}", "messages.json")
                            with open(file_path, 'w') as json_file:
                                json.dump(json.loads(answer), json_file, indent=4)
                                print(f'{C_GREEN}Translated to {currentLangName} ({lang}) dest: {C_GREEN.OFF}{C_BLUE}{PATH_TO_RESULT}{lang}/messages.json{C_BLUE.OFF}, delay for next: {delay}s' + '\n--------------')
                        except:
                            print(f'{C_RED}GPT Answer is not a valid JSON. Skipping...{C_RED.OFF}')
                    else:
                        print(f'{C_RED}Not a valid response. Skipping...{C_RED.OFF}')
                    # then reseat the thread and sleep delay
                    chatgpt.reset_thread()
                    time.sleep(delay)