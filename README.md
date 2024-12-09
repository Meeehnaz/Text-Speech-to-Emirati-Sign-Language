# Text and Speech to Emirati Sign Language Conversion App

This project demonstrates a **Text and Speech to Emirati Sign Language (ESL)** conversion app built using **Streamlit**, **Azure OpenAI**, and **Sentence Transformers** for semantic embeddings. The app processes text or speech input to convert it into the appropriate ESL video. It utilizes precomputed embeddings of ESL videos to find the best match for the given input, facilitating accurate sign language representation.

---

## Key Features

1. **Input Options**:
   - Text input for users to type their message in both English and Emirati Arabic.
   - Speech-to-text functionality for users to speak and have their words transcribed.
   
2. **Conversion to ESL**:
   - Input (text or speech) is converted into embeddings using a transformer model:  
     `sentence-transformers/all-MiniLM-L6-v2`.
   - Precomputed embeddings of ESL videos are matched with the input embeddings to identify the closest match.
   - Azure OpenAI is used to further refine the search.

3. **Video Mapping**:
   - Each word or phrase in ESL has a corresponding video. Once a match is found, the associated video is displayed to represent the sign language translation.

4. **Interactive UI**:
   - Built with **Streamlit**, ensuring a clean, user-friendly interface for seamless interaction.

---

## Technical Workflow

1. **Input Processing**:
   - Text: User types the message.
   - Speech: Speech-to-text conversion is handled.

2. **Embedding Generation**:
   - Text input or transcribed speech is converted into embeddings using the pre-trained transformer model:  
     `sentence-transformers/all-MiniLM-L6-v2`.

3. **Semantic Similarity Matching**:
   - The embeddings are compared with precomputed embeddings of ESL videos using similarity metrics (cosine similarity), Azure OpenAI further refines the search.
   - The closest matching video embedding is selected.

4. **Video Retrieval**:
   - The matched ESL video is retrieved and displayed on the app.

---

## Requirements

### Libraries and Tools
- **Python 3.8+**
- **Streamlit**: For building the UI.
- **sentence-transformers**: For generating text embeddings.
- **Azure OpenAI**: For natural language processing.
- **MoviePy**: For handling and displaying video outputs.

### Precomputed Data
- Embeddings for each ESL video should be precomputed and stored in a format like CSV or a json.
- Example format:  
  ```
  Video_ID, Word/Phrase, Embedding_Vector
  ```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/text-to-sign-language.git
   cd text-to-sign-language
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Azure OpenAI:
   - Add your Azure OpenAI API key to an `.env` file:
     ```plaintext
     AZURE_OPENAI_KEY=your_api_key
     AZURE_OPENAI_ENDPOINT=your_endpoint
     ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. Launch the app.
2. Select your input type (text or speech).
3. Enter text in the text box or use the microphone button for speech input.
4. Click **Convert**.
5. The corresponding ESL video will be displayed.

---

## Future Enhancements

- Enhance accuracy by fine-tuning embeddings for Emirati dialects.
- Explore advanced matching techniques or larger models for better semantic understanding.
- Provide an option for users to upload custom text files for batch processing.

---

## Contribution

Contributions are welcome! If you have ideas or improvements, feel free to fork the repository and create a pull request.

---

