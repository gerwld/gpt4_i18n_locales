"""Entry-point, translates every locale from languages.txt based on the reference (messages.json)"""
import os
import time
import json
import random

from tools.handlers.gptHandler import ChatGPTHandler
from tools.validators.isLocaleValid import isLocaleValid
from tools.handlers.auth import GPT_AUTH
from global_context import PATH_TO_RESULT, PATH_TO_RESULT_CHUNKS, C_GREEN, C_RED, C_BLUE, PRODUCT_NAME

import chromedriver_autoinstaller
try:
    chromedriver_autoinstaller.install()
except Exception as e:
    print(f"{C_RED}Error during ChromeDriver update: {e}{C_RED.OFF}")


# MESSAGE_PART1 = 'Translate to '
# MESSAGE_PART2 = f'. Respond only with result in ```, keep "{PRODUCT_NAME}" word untouched.:\n'
MESSAGE_PART1 = 'TRANSLATE TO '
MESSAGE_PART2 = F'. ANSWER ONLY WITH RESULT IN ```:\n'

CHUNKS_AMOUNT = 5

while True: 
    with open("languages.txt", "r") as file:
        languages = file.read().splitlines()
        localesList = [item.split(":")[0] for item in languages]
        print('-'*90 + f'\n{C_GREEN}GPT4_locales start: {C_RED}CHUNK MODE{C_RED.OFF}. Languages.txt total: {len(localesList)}{C_GREEN.OFF}')

        # checks PATH_TO_RESULT_CHUNKS for non-existing translations
        completed = []
        try: 
            completed = os.listdir(PATH_TO_RESULT) 
        except: pass
        todoLangList = [i for i in localesList if i not in completed]
        print('-'*90 + f'\n{C_BLUE}To-do: {len(todoLangList)}{C_BLUE.OFF} ({todoLangList}). \n{C_GREEN}Completed locales in {PATH_TO_RESULT}:{C_GREEN.OFF} {len(completed)} {f"({completed})" if len(completed) else ""}')

        # if not all translations were created, then read messages.json and translate not translated yet
        if len(todoLangList) > 0:
            with open("messages.json", "r") as file:
                originalLocale = file.read()

                # Load the JSON object
                json_data = json.loads(originalLocale)

                # Split the JSON object into two roughly equal parts
                json_parts = [json.dumps({key: json_data[key] for i, key in enumerate(json_data) if (i // (len(json_data) // CHUNKS_AMOUNT + 1)) == part}) for part in range(CHUNKS_AMOUNT)]
                

                chatgpt = ChatGPTHandler(*GPT_AUTH, strip_first_3 = True)
                for lang in todoLangList:
                    result = []
                    currentLangName = [mask for mask in languages if mask.startswith(lang)][0].split(":")[1]

                    # go over each json_chunk...
                    for i, json_chunk in enumerate(json_parts):
                        delay = random.randint(1, 4)
                        print(f'{C_GREEN}Working with: {lang}, part #{i + 1} ...{C_GREEN.OFF}')
                        gptRequest = f"{MESSAGE_PART1}{currentLangName} ({lang}){MESSAGE_PART2}{json_chunk}"

                        answer = chatgpt.interact(gptRequest)

                        # if response is valid, then create PATH_TO_RESULT_CHUNKS/lang/message.json with response
                        # if not skip to another lang
                        if str(answer):
                            if json.dumps(answer).strip() == json.dumps(json_chunk).strip():
                                print(f"{C_RED}Chunk was not translated. Skipping...")
                                chatgpt.reset_thread()
                                time.sleep(delay)
                                break;
                            try:
                                result.append(answer)
                                print(f'{C_GREEN}Translated chunk to {currentLangName} ({lang}), chunk {C_GREEN.OFF}{C_BLUE}chunk #0{i + 1}{C_BLUE.OFF}, delay for next: {delay}s' + '\n--------------')
                            except:
                                print(f"{C_RED}Invalid JSON chunk. Skipping...{C_RED.OFF}")
                                chatgpt.reset_thread()
                                time.sleep(delay)
                                break;
                        else:
                            print(f'{C_RED}Not a valid response. Skipping...{C_RED.OFF}')
                            chatgpt.reset_thread()
                            time.sleep(delay)
                            break;
                        # then reseat the thread and sleep delay
                        chatgpt.reset_thread()
                        time.sleep(delay)
                

                    # after foreach validate result combined from chunks and add it.
                    if len(result) == CHUNKS_AMOUNT:
                        try:
                            combined_json = None
                            try:
                                combined_json = json.dumps({k: v for json_str in result for k, v in json.loads(json_str).items()}, indent=2)
                                print(combined_json) 
                            except:
                                pass;
                            if combined_json and isLocaleValid(str(originalLocale), str(combined_json)):
                                try:                    
                                    if not os.path.exists(f"{PATH_TO_RESULT_CHUNKS}{lang}"):
                                        os.makedirs(f"{PATH_TO_RESULT_CHUNKS}{lang}")
                                    file_path = os.path.join(f"{PATH_TO_RESULT_CHUNKS}{lang}", "messages.json")
                                    with open(file_path, 'w') as json_file:
                                        json.dump(json.loads(combined_json), json_file, indent=4)
                                        print(f'{C_GREEN}Combined chunks for {currentLangName} ({lang}), dest: {C_GREEN.OFF}{C_BLUE}{PATH_TO_RESULT_CHUNKS}{lang}/messages.json{C_BLUE.OFF}, delay for next: {delay}s' + '\n--------------')
                                except:
                                    print(f'{C_RED}Chunks combining error.{C_RED.OFF}')
                            else:
                                print(f'{C_RED}Some of the chunks is not valid. Skipping...{C_RED.OFF}')
                        except:
                            print(f'{C_RED}Chunks combining error #0000000.{C_RED.OFF}')