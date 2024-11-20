# Effectz-VLM-OCR by [Effectz.AI](https://www.effectz.ai/)  ![Logo of Effectz.AI](https://github.com/effectz-ai/Effectz_VLM_OCR/blob/main/img/effectzai.png)

## Welcome to Effectz-VLM-OCR
### Effectz-VLM-OCR => Convert Documents and Images into Markdown Format with VLMs 
Effectz-VLM-OCR helps you easily convert documents and images into markdown format powered by **Vision Language Models (VLMs)**. You can customize the VLM and the system prompt too.


- [💾 Effectz-VLM-OCR Walkthrough](#effectz-vlm-ocr-walkthrough)
- [✨ Feature Lists](#feature-lists)
- [🔑 API Keys and Variables](#api-keys-and-variables)


## Effectz-VLM-OCR Walkthrough

### Setup The Environment

```
poetry install
poetry shell
```

### Run Effectz-VLM-OCR

```
python main.py
```

### Convert Your Documents and Images Into .md Format

```
curl -X POST http://localhost:5001/api/get_markdown \
  -F "file=@your_file" \
  -F "vlm=your_vlm" \
  -F "system_prompt=your_system_prompt"
```


## Feature Lists

| 🤖 Model Support                       | Implemented | Description                  |
| -------------------------------------- | ----------- | ---------------------------- |
| Ollama (e.g. llama3.2-vision:11b)      | ✅         | Local VLMs powered by Ollama |

| 📁 Supported Document/Image Types             | Implemented | Description                                      |
| --------------------------------------------- | ----------- | ------------------------------------------------- |
| PDF                                           | ✅         | PDF files can be converted into .md format        |
| DOCX                                          | ✅         | DOCX files can be converted into .md format       |
| JPG/JPEG                                      | ✅         | JPG/JPEG files can be converted into .md format   |
| PNG                                           | ✅         | PNG files can be converted into .md format        |

| 🆒 Cool Bonus         | Implemented | Description                                             |
| --------------------- | ----------- | ------------------------------------------------------- |
| Docker Support        | ✅         | Effectz-VLM-OCR is deployable via Docker                |


## API Keys and Variables

Below is a comprehensive list of the API keys and variables you may require:

| Environment Variable   | Value                                                      | Description                                                                       |
| ---------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------- |
| APP_HOST               | Your address to start the app                              | Set address                                                                       |
| APP_PORT               | Your port to start the app                                 | Set port                                                                          |
| VLM                    | Your VLM name                                              | Set VLM                                                                           |
| SYSTEM_PROMPT          | Your system prompt                                         | Set system prompt                                                                 |

