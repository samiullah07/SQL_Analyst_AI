from sqlalchemy import create_engine, inspect
import json
import sqlite3


db_url = 'sqlite:///amazon.db'
def extreact_schema(db_url):
    engine = create_engine(db_url)
    inspector = inspect(engine)
    schema = {}


    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [column['name'] for column in columns]
    return json.dumps(schema)



## LLm and Langchain

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import re


def text_to_sql(query, schema_json):

    model = OllamaLLM(model="deepseek-r1:8b")
  


    prompt_template = """
    You are an expert SQL generator. Given the database schema and a natural language query, generate the corresponding SQL query.

    Database Schema:
    {schema}

    Natural Language Query:
    {query}

    SQL Query:
    """

    prompt = ChatPromptTemplate.from_messages([
        {"role": "system", "content": prompt_template},
        {"role": "user", "content": "\n\nSchema : {schema}\n\n Question {query}\n\n SQL:"}
    ])

    chain = prompt | model
    raw_response = chain.invoke({ 
        "schema": schema_json,
        "query": query
    })
    sql_query = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL).strip()
    return sql_query.strip()




def get_data_from_db(natural_language_query):
    schema = extreact_schema(db_url)
    sql_query = text_to_sql(natural_language_query, schema)
    


    ## Execute the generated SQL query
    conn = sqlite3.connect('amazon.db')
    cursor = conn.cursor()
    results = cursor.execute(sql_query)
    response = results.fetchall()
    conn.close()
    return response
