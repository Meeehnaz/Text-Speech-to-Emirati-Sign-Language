import json
import numpy as np
from embeddings import get_embeddings
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
from env import client

phrase_video_dict = {
    "how are you": "how_are_you",
    # "good morning": "GoodMorning",
    # "good evening": "GoodEvening",
    # "Date of Birth": "DateOfBirth"
    }


# Load the video embeddings from the JSON file
with open('video_embeddings_main.json', 'r') as f:
    video_embeddings = json.load(f)

def preprocess_text(text):
    """Preprocess text by converting it to lowercase and removing punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  
    return text

def check_semantic_similarity(word1, word2):
    """Check if two words are semantically similar using Azure OpenAI."""
    try:
        print("1")
        messages = [
            {"role": "system", "content": f"Are the words '{word1}' and '{word2}' semantically similar or interchangeable in context? Respond with 'yes' if they are similar or interchangeable, and 'no' if they are not."}
        ] 
        print("2")
        response = client.chat.completions.create(
            model='gpt-4',
            messages=messages,
            temperature=0.5,
            # max_tokens=150,
        )
        print("3")
        answer = response.choices[0].message.content.strip()
        print("4")
        print(answer)
        return answer.lower() == "yes"
    except Exception as e:
        print(f"Error with Azure OpenAI API: {e}")



def find_most_similar_video_for_word(word, similarity_threshold=0.6):

    word_embedding = get_embeddings(word)
    word_embedding_list = word_embedding.cpu().numpy().reshape(1, -1)  # Convert to 2D array for similarity calculation

    max_similarity = -1  # Start with a very low similarity score
    best_match_video = None
    best_match_word = None

    # Iterate over the video embeddings
    for key_word, data in video_embeddings.items():
        video_embedding = np.array(data['embedding']).reshape(1, -1)  # Convert embedding to 2D array

        # Calculate cosine similarity
        similarity = cosine_similarity(word_embedding_list, video_embedding)[0][0]

        # Keep track of the best match
        if similarity > max_similarity:
            max_similarity = similarity
            best_match_video = os.path.splitext(os.path.basename(data['video_path']))[0]
            best_match_word = key_word

    # Check similarity conditions
    if max_similarity < similarity_threshold and max_similarity >= 0.46:
        if check_semantic_similarity(word, best_match_word):
            return best_match_video, max_similarity  
        else:
            return None, max_similarity  
    elif max_similarity >= similarity_threshold:
        return best_match_video, max_similarity  # Retain video if similarity is above threshold

    return None, max_similarity  # Exclude if similarity is below 0.4



def translate_sentence_to_videos(user_input, similarity_threshold=0.8):
    processed_input = preprocess_text(user_input)

    video_sequence = []

    # First, check for common phrases
    for phrase, video in phrase_video_dict.items():
        if phrase in processed_input:
            video_sequence.append(video)  # Add the video for the matched phrase
            processed_input = processed_input.replace(phrase, '')  # Remove matched phrase from input
            print(f"Matched phrase '{phrase}' with video '{video}'")
    
    # After removing phrases, tokenize the remaining words
    words = processed_input.split()

    # For each word in the sentence, find the most similar video
    for word in words:
        if word.strip():  # Ensure word is not empty after phrase removal
            best_video, similarity = find_most_similar_video_for_word(word, similarity_threshold)
            
            if best_video:
                video_sequence.append(best_video)  # Add the best matching video to the sequence
                print(f"Video sequence for word '{word}':", video_sequence)
            else:
                print(f"No suitable video found for the word '{word}' (similarity: {similarity:.2f})")

    return video_sequence



