"""Entry-point, translates every locale from languages.txt based on the reference (messages.json)"""
import os
import time
import random

from tools.handlers.gptHandler import ChatGPTHandler
from tools.validators.isDescriptionValid import isDescriptionValid
from tools.handlers.auth import GPT_AUTH
from global_context import PATH_TO_RESULT_DESC, C_GREEN, C_RED, C_BLUE, PRODUCT_NAME

import chromedriver_autoinstaller
try:
    chromedriver_autoinstaller.install()
except Exception as e:
    print(f"{C_RED}Error during ChromeDriver update: {e}{C_RED.OFF}")

MESSAGE_PART1 = 'Translate to '
MESSAGE_PART2 = f'. Keep "##", Answer only with result in ``` not as JSON:\n\n'

def remove_prefix(input_str, prefix):
    if input_str.startswith(prefix):
        return input_str[len(prefix):]
    return input_str

while True: 
    with open("languages.txt", "r") as file:
        languages = file.read().splitlines()
        localesList = [item.split(":")[0] for item in languages]
        print('-'*90 + f'\n{C_GREEN}GPT4_locales start: {C_RED}DESC MODE{C_RED.OFF}. Languages.txt total: {len(localesList)}{C_GREEN.OFF}')

        # checks PATH_TO_RESULT_DESC for non-existing translations
        completed = []
        try: 
            completed = [file.split('_')[1].replace('.txt', '') for file in os.listdir(PATH_TO_RESULT_DESC) if file.endswith('.txt')]
        except: pass
        todoLangList = [i for i in localesList if i not in completed]
        print('-'*90 + f'\n{C_BLUE}To-do: {len(todoLangList)}. {C_BLUE.OFF}{C_GREEN}Completed locales in {PATH_TO_RESULT_DESC}:{C_GREEN.OFF} {len(completed)} {f"({completed})" if len(completed) else ""}')

        # if not all translations were created, then read messages.json and translate not translated yet
        if len(todoLangList) > 0:
            with open("description.txt", "r") as file:
                originalLocale = file.read()

                chatgpt = ChatGPTHandler(*GPT_AUTH, strip_first_3 = True)
                for lang in todoLangList:
                    currentLangName = [mask for mask in languages if mask.startswith(lang)][0].split(":")[1]
                    delay = random.randint(1, 4)
                    print(f'{C_GREEN}Working with: {lang}...{C_GREEN.OFF}')
                    gptRequest = f"{MESSAGE_PART1}{currentLangName} ({lang}){MESSAGE_PART2}{originalLocale}"
                    answer = chatgpt.interact(gptRequest)

                    # if response is valid, then create PATH_TO_RESULT_DESC/lang/message.json with response
                    if isDescriptionValid(answer):
                        try:                    
                            if not os.path.exists(f"{PATH_TO_RESULT_DESC}"):
                                os.makedirs(f"{PATH_TO_RESULT_DESC}")
                            file_path = os.path.join(f"{PATH_TO_RESULT_DESC}", f"{currentLangName}_{lang}.txt")
                            with open(file_path, 'w+') as w:
                                w.write(remove_prefix(str(answer), "## ").replace('```', '').replace('Copy Code', ''))
                                print(f'{C_GREEN}Translated to {currentLangName} ({lang}) dest: {C_GREEN.OFF}{C_BLUE}{PATH_TO_RESULT_DESC}{currentLangName}_{lang}.txt{C_BLUE.OFF}, delay for next: {delay}s' + '\n--------------')
                        except:
                            print(f'{C_RED}GPT Answer is not a valid, check string 50 in generate_desc.py for more info. Skipping...{C_RED.OFF}')
                    else:
                        print(f'{C_RED}Not a valid response. Skipping...{C_RED.OFF}')
                    # then reseat the thread and sleep delay
                    chatgpt.reset_thread()
                    time.sleep(delay)