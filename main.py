# Step 1: Extract Schema
from sqlalchemy import create_engine, inspect
import json
import re
import sqlite3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_FILE = "Amazon.db"
db_url = f"sqlite:///{DB_FILE}"


def extract_schema(db_url):
    engine = create_engine(db_url)
    inspector = inspect(engine)
    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col["name"] for col in columns]

    return json.dumps(schema, indent=2)


# -----------------------------------------------------------
# Step 2: Text → SQL using GROQ API
# -----------------------------------------------------------

def groq_chat_completion(prompt, model="llama-3.1-8b-instant"):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    response = requests.post(url, json=body, headers=headers).json()

    try:
        return response["choices"][0]["message"]["content"]
    except:
        raise ValueError(f"GROQ API Error: {response}")


def text_to_sql(schema, prompt):

    SYSTEM_PROMPT = """
You are an expert SQLite SQL generator.

Strict rules:
- Use ONLY tables and columns from schema
- Output ONLY valid SQLite SQL query
- No markdown
- No explanation
- No comments
- No <think>
"""

    final_prompt = f"""
{SYSTEM_PROMPT}

Schema:
{schema}

Question:
{prompt}

Return ONLY SQL:
"""

    print("\n Sending prompt to llm...")
    raw_response = groq_chat_completion(final_prompt)

    print("\n RAW Groq Output:\n", raw_response)

    # remove hidden tags
    cleaned = re.sub(r"<think>.*?</think>", "", raw_response, flags=re.DOTALL).strip()

    # ensure ending semicolon
    if not cleaned.endswith(";"):
        cleaned += ";"

    sql = cleaned.split("\n")[0]

    print("\n Final SQL Query:\n", sql)
    return sql


# -----------------------------------------------------------
# Step 3: Run SQL on Local SQLite Database
# -----------------------------------------------------------

def get_data_from_database(prompt):

    print("\n Extracting Schema...")
    schema = extract_schema(db_url)

    print("\n Converting Text → SQL using Groq...")
    sql_query = text_to_sql(schema, prompt)

    print("\n Executing SQL on Amazon.db...")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        res = cursor.execute(sql_query)
        results = res.fetchall()
    except Exception as e:
        conn.close()
        print("\n SQL Error:", e)
        return f"SQL Error: {e}"

    conn.close()
    return results
