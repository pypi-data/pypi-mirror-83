# customner

This is an nlp library which used to convert the tsv file format to required format for Name Entity Recognition

## Installation

Run the following to install:

```python
pip install customner
```

## Usage

```python
import customner

# Generate training set as per spacy format for medical dataset
training_data,unique_labels=load_spacy_data(tsv_file_path)
```
