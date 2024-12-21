# BitFest_Hackathon
# Banglish to Bengali Translator

This repository contains `challenge1.ipynb`, a notebook that trains a Banglish-to-Bengali transliteration model using Facebook mBART. The model is fine-tuned on Banglish-Bengali data for accurate transliteration.

## Features
- Preprocesses Banglish text.
- Fine-tunes mBART for transliteration.
- Provides a transliteration function for inference.

## Requirements
- Python 3.7+, PyTorch, Hugging Face Transformers & Datasets, scikit-learn, pandas

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/banglish-to-bengali-translator.git
   cd banglish-to-bengali-translator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Open and run `challenge1.ipynb` in Jupyter Notebook to train the model.
2. The trained model is saved in `./final_model`.

### Example Translation
Load the model and translate:
```python
model = AutoModelForSeq2SeqLM.from_pretrained("./final_model").to(device)
tokenizer = AutoTokenizer.from_pretrained("./final_model")
example_translation = translate_banglish_to_bengali("ami tomake valobashi", model, tokenizer, device)
print(example_translation)
```

## Dataset
Uses `SKNahin/bengali-transliteration-data` from Hugging Face with Banglish-Bengali pairs.

## Training Details
- Model: `facebook/mbart-large-50`
- Epochs: 8, Batch Size: 8, Learning Rate: 3e-5
- Mixed-precision FP16 training.

## Model Hosting
The trained model is available on Hugging Face:
[Banglish to Bengali Model](https://huggingface.co/nowshining/banglishtobang)

## Acknowledgments
- Hugging Face for `transformers` and `datasets` libraries.
- Facebook AI for mBART.
- Dataset: `SKNahin/bengali-transliteration-data`.

---
Contributions and issues are welcome!

