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

## Testing
```
pytest
```
