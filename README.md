# Folder Organizer

This project summarizes folders and generates metadata using local Ollama models.

## Installation
```
conda env create -f environment.yml
conda activate folder-organizer
pip install -e .

The environment installs `langchain-ollama` and `docx2txt` for model access and
DOCX support. Before running the application you must pull an Ollama model:
```bash
ollama pull llama2
```

## Usage
```
python examples/run_example.py --path /path/to/folder
```

After showing the generated summary the CLI now provides interactive options:

* **a**ccept - use the summary and generate metadata
* **r**egenerate - run summarization again
* **e**dit - edit the summary text manually
* **c**ancel - exit without generating metadata

## Testing
```
pytest
```
