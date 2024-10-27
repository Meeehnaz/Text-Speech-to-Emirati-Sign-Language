import os
import json
import numpy as np
from embeddings import get_embeddings  


video_folder = "ESL_Processed"

def create_video_embedding_dataset():
    video_embeddings = {}

    # Check if the video folder exists
    if not os.path.exists(video_folder):
        print(f"Video folder '{video_folder}' not found.")
        return
    
    # Loop through the video files in the folder
    for video_name in os.listdir(video_folder):
        if video_name.endswith(".mp4"): 
            word = video_name.split(".")[0]  
            print(f"Processing: {word}")
            
            embedding = get_embeddings(word)
            embedding_list = embedding.cpu().numpy().tolist() if isinstance(embedding, np.ndarray) else embedding.tolist()

            video_embeddings[word] = {
                "video_path": os.path.join(video_folder, video_name),
                "embedding": embedding_list
            }

    # Save the embedding dataset to a JSON file
    with open('video_embeddings_main.json', 'w') as f:
        json.dump(video_embeddings, f)

    print("Embeddings saved to 'video_embeddings.json'.")

create_video_embedding_dataset()