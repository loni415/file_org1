# Folder Organizer

This project summarizes folders and generates metadata using local Ollama models.

## Installation
```
conda env create -f environment.yml
conda activate folder-organizer
pip install -e .
```

The environment installs `docx2txt` so DOCX files can be processed.

## Usage
```
python examples/run_example.py --path /path/to/folder
```

## Testing
```
pytest
```
