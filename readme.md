# gpt4_i18n_locales

Translates i18n locales to any language supported by ChatGPT. This project is primarily aimed at developing a bot that utilizes GPT-4 "as it is", with automatization and without using OpenAI API, which is significantly more expensive than $25. Currently, it may not be "perfectly shaped", so if you want to make some improvements feel free to contribute. (However, please understand that I may not accept changes that are not beneficial).

<img width="1280" alt="Pasted Graphic 1" src="https://github.com/gerwld/gpt4_locales/assets/47056812/7562d6ed-3ea4-445b-b64b-3775c923c95f">


<br>

## What currently works:
- GPT3.5 / GPT 4, just set a prop. value to the GPT Handler
- Auto-detection when chat.openai.com "slips" to GPT 3.5, so it doesn't mix up content from 3.5 and 4.
- Auto-clicking the "keep going" button / "keep going" message request (handling is as less buggy as it can be)
- Binding all answer chunks into one big chunk if the answer is valid, or skipping it.
- Random delay each time, to reduce limit messages appearing.
- Skipping at the beginning of generation if the generated answer does not start with a chosen value (\<article\>, any preferred).

<br><br>

## Init project:

```
git clone git@github.com:gerwld/gpt4_i18n_locales.git && cd gpt4_i18n_locales
pip: -r requirements.txt
```
 
## Tools:

### Translate JSON to lang selected it languages.txt (ln:mask):

```
python -m tools.generate
```
 
### Same as previous, but generates from chunks. More stable, but translation has less context:

```
python -m tools.generate_chunks
```

### generate_desc for description translate. isDescriptionValid for percise validation:

```
python -m tools.generate_desc
```

### utf16to8:

```
python -m tools.utf16to8
```

### get unused JSON keys in comparsion of 2 files:

```
python -m tools.json.get_unused_i18n
```

### combine JSON files into 1:

```
python -m tools.json.combine
```

### remove keys from all locales in dir:

```
python -m tools.json.remove_keys
```



<br>

## To run improvers:

### ChatGpt:

```
python -m improvers.chatGPT
```

