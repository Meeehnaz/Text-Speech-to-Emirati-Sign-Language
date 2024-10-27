from transformers import MarianMTModel, MarianTokenizer

# Load the model and tokenizer
model_name = "Helsinki-NLP/opus-mt-ar-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Function to translate text
def translate_arabic_to_english(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    
    # Perform translation
    translated = model.generate(**inputs)
    
    # Decode the output
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text


