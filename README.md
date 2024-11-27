# Effectz-VLM-OCR by [Effectz.AI](https://www.effectz.ai/)  ![Logo of Effectz.AI](https://github.com/effectz-ai/Effectz_VLM_OCR/blob/main/img/effectzai.png)

## Welcome to Effectz-VLM-OCR
### Effectz-VLM-OCR => Convert Documents and Images into Markdown Format with VLMs 
Effectz-VLM-OCR helps you easily convert documents and images into markdown format powered by **Vision Language Models (VLMs)**. You can customize the system prompt, the markdown generation model type and the layout detection model type too.


- [💾 Effectz-VLM-OCR Walkthrough](#effectz-vlm-ocr-walkthrough)
- [✨ Feature Lists](#feature-lists)
- [🔑 API Keys and Variables](#api-keys-and-variables)
- [📌 Special Notes](#special-notes)


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
  -F "system_prompt=your_system_prompt" \
  -F "markdown_model_type=your_markdown_model_type"
```

### Convert Your Documents and Images Into .md Format (Layout entity wise)

```
curl -X POST http://localhost:5001/api/layout_entity_markdown \
  -F "file=@your_file" \
  -F "system_prompt=your_system_prompt" \
  -F "markdown_model_type=your_markdown_model_type" \
  -F "layout_model_type=your_layout_model_type"
```


## Feature Lists

| 🤖 VLM/MLLM Support                    | Implemented | Description                  |
| -------------------------------------- | ----------- | ---------------------------- |
| Ollama (e.g. llama3.2-vision:11b)      | ✅         | Local VLMs powered by Ollama |
| OpenAI (e.g. gpt-4o-mini)              | ✅         | MLLMs by OpenAI              |

| 🤖 Layout Detection Support                              | Implemented | Description                             |
| -------------------------------------------------------- | ----------- | --------------------------------------- |
| Azure Layout                                             | ✅         | Azure Layout service                    |
| Hugging Face models(e.g. cmarkea/detr-layout-detection)  | ✅         | Layout detection models in Hugging Face |

| 📁 Supported Document/Image Types             | Implemented | Description                                      |
| --------------------------------------------- | ----------- | ------------------------------------------------- |
| PDF                                           | ✅         | PDF files can be converted into .md format        |
| DOCX                                          | ✅         | DOCX files can be converted into .md format       |
| JPG/JPEG                                      | ✅         | JPG/JPEG files can be converted into .md format   |
| PNG                                           | ✅         | PNG files can be converted into .md format        |

| 🆒 Cool Bonus                 | Implemented | Description                                                        |
| ----------------------------- | ----------- | ------------------------------------------------------------------ |
| Docker Support                | ✅         | Effectz-VLM-OCR is deployable via Docker                           |
| Layout Entity Wise Conversion | ✅         | Convert documents and images into .md format (layout entity wise)  |


## API Keys and Variables

Below is a comprehensive list of the API keys and variables you may require:

| Environment Variable           | Value                                                      | Description                                                                       |
| ------------------------------ | ---------------------------------------------------------- | --------------------------------------------------------------------------------- |
| APP_HOST                       | Your address to start the app                              | Set address                                                                       |
| APP_PORT                       | Your port to start the app                                 | Set port                                                                          |
| SYSTEM_PROMPT                  | Your system prompt                                         | Set system prompt                                                                 |
| LAYOUT_DETECTION_MODEL_TYPE    | Your layout detection model type                           | Set layout detection model type                                                   |
| AZURE_KEY                      | Your Azure key                                             | Set Azure key                                                                     |
| MARKDOWN_GENERATION_MODEL_TYPE | Your markdown generation model type                        | Set layout detection model type                                                   |
| OPENAI_KEY                     | Your OpenAI key                                            | Set OpenAI key                                                                    |

## Special Notes

- If you're using [Ollama](https://ollama.com/) for VLMs (markdown generation), you have to launch the Ollama app or open the terminal and type 'ollama serve' first.
- If you're using a Hugging Face model as the layout detection model, when you run Effectz-VLM-OCR for the first time, the model will be downloaded and stored. By default the models are downloaded and stored in:
  - Linux/MacOS: ~/.cache/huggingface/transformers/
  - Windows: C:\Users\YourUsername\.cache\huggingface\transformers\
