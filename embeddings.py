from transformers import AutoTokenizer, AutoModel
import torch

# Load pre-trained model and tokenizer
model_name = 'sentence-transformers/all-MiniLM-L6-v2'  # You can choose other models as well
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to get embeddings
def get_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)  # Mean pooling
    return embeddings

