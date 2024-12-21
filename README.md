# BitFest_Hackathon
# Challenge 1
# Banglish to Bengali Translator

The Challenge1 Folder in the repository contains `challenge1.ipynb`, a notebook that trains a Banglish-to-Bengali transliteration model using Facebook mBART. The model is fine-tuned on Banglish-Bengali data for accurate transliteration.

## Features
- Preprocesses Banglish text.
- Fine-tunes mBART for transliteration.
- Provides a transliteration function for inference.

## Requirements
- Python 3.7+, PyTorch, Hugging Face Transformers & Datasets, scikit-learn, pandas

## Installation
1. Clone the repository:
 2. Install dependencies:
 

## Usage
1. Open and run `Challenge1.ipynb` in Jupyter Notebook to train the model.
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

# Challenge 2
# Ingredients and Recipe Chatbot

The project folder contains `database.py` and `main.py` files, implementing a chatbot that recommends recipes based on user input and available ingredients. The solution leverages OpenAI's API and FastAPI framework for intelligent interaction.

---

## Features
- Processes user preferences (e.g., "I want something sweet").
- Matches user preferences with available ingredients and recipes.
- Uses OpenAI's GPT for natural language understanding.
- Provides real-time recommendations via a FastAPI endpoint.

---

## Requirements
- Python 3.5+
- FastAPI, SQLAlchemy, OpenAI Python SDK, Uvicorn

---

## Installation
1. Clone the repository:
   
2. Install dependencies:
   ```bash
   pip install pip install fastapi uvicorn sqlalchemy pydantic openai
   ```

---

## Usage
1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
2. Interact with the chatbot using the `/chat` endpoint:
   ```json
   POST /chat
   {
       "user_input": "I want something sweet"
   }
   ```

### Example Output
If the user inputs:
```json
{
    "user_input": "I want something sweet"
}
```
The chatbot might respond:
```json
{
    "response": "Based on your preferences and available ingredients like sugar and chocolate, we recommend 'Chocolate Cake' or 'Sweet Pancakes'."
}
```

---

## Dataset
- **Recipes Table:** Contains recipe names and associated ingredients.
- **Ingredients Table:** Lists ingredients available to the user.

---

## Implementation Details

### NLP Matching
The chatbot uses a `keyword_map` to understand user preferences, mapping words like "sweet" to ingredients such as `sugar` and `honey`.

### FastAPI Endpoint
The `/chat` endpoint handles user input:
1. Extracts user preferences using keywords.
2. Queries the database for recipes that match the preferences.
3. Filters recipes based on available ingredients.
4. Generates a response using OpenAI’s GPT model.



## Training Details
- **Model:** OpenAI’s GPT-3.5
- **Dataset:** Recipe and ingredient data stored in a relational database.
- **NLP Matching:** Custom keyword-based mapping for preferences.

---

## Model Hosting
The solution does not require hosting a custom model as it integrates OpenAI’s GPT API directly.

---

## Acknowledgments
- **FastAPI:** Framework for creating APIs.
- **OpenAI GPT:** Natural language processing.
- **SQLAlchemy:** Database ORM for handling recipes and ingredients.


