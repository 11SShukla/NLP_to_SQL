# NLP_to_SQL
# NLP_to_SQL
This project converts natural language questions into executable SQL queries using a lightweight LLM
.

├── create_database.py      # Creates / loads Amazon.db

├── main.py                 # Backend logic: schema, LLM call, SQL execution

├── frontend.py             # Streamlit UI

├── Amazon.db               # SQLite sample database

├── README.md

├── requirements.txt

└── .env                    # GROQ_API_KEY=xxxx
Installation & Setup

Follow these steps to run the project locally:

1️⃣ Clone the Repository
git clone <your-repo-url>
cd <repo-folder>

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Add Your GROQ API Key

Create a .env file:

GROQ_API_KEY=your_key_here

4️⃣ Create the Database
python create_database.py


This will generate/initialize Amazon.db.

5️⃣ Run the Backend Logic
python main.py

6️⃣ Launch the Frontend
streamlit run frontend.py

#Future Improvements

Add query validation
Add multi-table join handling
Add conversation memory
Add role-based authentication
Deploy Streamlit app online
