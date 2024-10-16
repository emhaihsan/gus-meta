# Gus Meta - Islam and Quran Chatbot

Gus Meta is a chatbot application designed to answer questions related to Islam and the Quran. This project uses AI technology to provide users with accurate and informative answers.

## Main Features

- User-friendly chat interface
- Ability to answer questions about Islam and the Quran
- User reaction system (like, dislike, regenerate answers)
- Knowledge storage and reuse from previous interactions
- Monitoring dashboard for analyzing user reactions

## Technologies Used

- Backend: FastAPI, Python
- Frontend: HTML, CSS, JavaScript
- Database: PostgreSQL with pgvector extension
- AI Model: LLaMA (Large Language Model)
- Monitoring: Streamlit

## Project Structure

```
.
├── backend/
│   ├── app.py
│   ├── init_db.py
│   └── monitoring_dashboard.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── requirements.txt
└── .gitignore
```

## How to Run the Project

1. Make sure you have installed all the dependencies listed in `requirements.txt`.

2. Initialize the database by running:

   ```
   python backend/init_db.py
   ```

3. Run the FastAPI backend:

   ```
   uvicorn backend.app:app --reload
   ```

4. Open the `frontend/index.html` file in your browser to access the chat interface.

5. To run the monitoring dashboard, use the command:
   ```
   streamlit run backend/monitoring_dashboard.py
   ```

## API Usage

The backend API provides several main endpoints:

- `/chat`: To send messages and receive responses from the chatbot
- `/react`: To add reactions to chatbot responses
- `/regenerate`: To request answer regeneration
- `/add_knowledge`: To add new knowledge to the system

For more details on how to use the API, please refer to the source code in `backend/app.py`.

## Related Links

- [Llama 3.2-3B Finetuned Bahasa Indonesia](emhaihsan/llama3.2-3B-Finetuned-Bahasa-Indonesia)
- [Gus Meta Model (Llama 3.2 Finetuned on Al-Qur'an text)](https://huggingface.co/emhaihsan/gus_meta_3.2_3b)
- [Quran Indonesia Tafseer and Translation](https://huggingface.co/datasets/emhaihsan/quran-indonesia-tafseer-translation)
- [Alpaca Cleaned Translated Id](https://huggingface.co/datasets/rubythalib33/alpaca-cleaned-translated-id)
