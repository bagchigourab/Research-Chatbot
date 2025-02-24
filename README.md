# Research-Chatbot
### 🚀 Objective
The Research-Chatbot is a powerful AI assistant built using a Large Language Model (LLM). It leverages LangChain, SQLite (SQLAlchemy) for data storage, Arxiv API for fetching research papers as a database for Retrieval-Augmented Generation (RAG), and GPT-4 as the core LLM.

### ✨ Key Features
Retrieval-Augmented Generation (RAG): Enhances chatbot responses with relevant research papers.
User Data Storage: Queries and interactions are stored in a SQLite database using SQLAlchemy.
Arxiv API Integration: Fetches relevant academic papers dynamically.
LLM-Powered Conversations: Uses OpenAI's GPT-4 for intelligent responses.
<div align="center">
  <img src="https://github.com/user-attachments/assets/e33a9370-8fcb-4842-9a81-c1045f42da4f" alt="image">
  <img src="https://github.com/user-attachments/assets/73d3832c-502a-4f07-840b-d327d73602f8" alt="image">
</div>


### Installation
**Clone the repository:**
```bash
git clone https://github.com/bagchigourab/Research-Chatbot
cd Research-Chatbot
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the chatbot server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
