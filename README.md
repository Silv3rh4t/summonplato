# SummonPlato

SummonPlato is a self-hosted Retrieval-Augmented Generation (RAG) based chatbot designed to answer questions using embedded knowledge from various sources. This project is built for experimentation and is intended to be the simplest possible RAG chatbot, with plans for future enhancements and versions focused on other philosophers.

## Features
- **RAG-based Chatbot**: Uses Retrieval-Augmented Generation to provide contextually relevant answers.
- **Self-Hosted**: Run entirely on your own infrastructure—no external dependencies for chat logic.
- **Data Pipeline**: Includes scripts to scrape, clean, chunk, embed, and store data using FAISS for efficient similarity search.
- **FastAPI Server**: Serves a static web interface for interacting with the chatbot.
- **Extensible**: Designed as a foundation for experimenting with new methods and creating chatbots for other philosophers.

## How it Works
1. **Data Preparation**: Scripts (such as `embed.py` and `scrape.py`) scrape, clean, chunk, and embed textual data.
2. **Embedding Storage**: Data embeddings are stored using [FAISS](https://github.com/facebookresearch/faiss) for fast vector search.
3. **Serving**: A FastAPI backend serves a static HTML/JS interface and exposes API endpoints for chat.

## Running the Chatbot
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Prepare your data using the provided scripts.
3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 3030
   ```
4. Open your browser and go to `http://localhost:3030` to use the chatbot.

## Customization & Experiments
This is a minimal RAG chatbot implementation. You are encouraged to experiment with new data sources, chunking strategies, embedding models, and retrieval techniques. Future versions will include chatbots for other philosophers and improved retrieval/generation methods.

## License
MIT License

---
This is a part of a larger project - Summon. Find out more about the current status of the project through:
`https://akhandyaduvanshi.in/summon` - Github Page for frontend only
`https://summon.akhandyaduvanshi.in/` - Low Uptime
*Summon is a work in progress. Contributions and ideas are welcome!*
