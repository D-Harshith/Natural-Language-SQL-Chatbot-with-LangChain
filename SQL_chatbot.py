# Import necessary libraries
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import re
import streamlit as st

# Load environment variables
load_dotenv()

# Configure Azure OpenAI settings
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the database connection
db_url = "mysql+mysqlconnector://root:1234@localhost:3306/Chinook"
db = SQLDatabase.from_uri(db_url)

# Function to extract schema information
def get_schema():
    return db.get_table_info()

# Function to clean SQL queries (remove markdown formatting)
def clean_sql_query(raw_query):
    if "```sql" in raw_query:
        match = re.search(r"```sql\n(.*?)```", raw_query, re.DOTALL)
        if match:
            return match.group(1).strip()
    return raw_query.strip()

# Function to execute SQL queries
def run_query(query):
    try:
        return db.run(query.strip())
    except Exception as e:
        return f"Error executing query: {e}"

# Define the prompt template for generating SQL queries
sql_template = """
Based on the below schema, write ONLY an SQL query that would answer the following question:

Schema:
{schema}

Question:
{question}

SQL Query:
"""
sql_prompt = ChatPromptTemplate.from_template(sql_template)

# Define the prompt template for generating natural language responses
response_template = """
Based on the below schema, question, SQL query, and SQL response, write a natural language response:

Schema:
{schema}

Question:
{question}

SQL Query:
{query}

SQL Response:
{response}
"""
response_prompt = ChatPromptTemplate.from_template(response_template)

# Initialize the LLM (Azure OpenAI)
llm = AzureChatOpenAI(
    deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
    temperature=0,
    cache=False,
    openai_api_key=OPENAI_API_KEY,
    openai_api_version=OPENAI_API_VERSION,
)

# Create the SQL generation chain
sql_chain = (
    RunnablePassthrough.assign(schema=lambda x: get_schema())
    | sql_prompt
    | llm.bind(stop=["\n SQL Result:"])
    | StrOutputParser()
    | clean_sql_query
)

# Create the full chain for generating natural language responses
full_chain = (
    RunnablePassthrough.assign(query=sql_chain)
    .assign(schema=lambda x: get_schema())
    .assign(response=lambda var: run_query(var.get("query", "")))
    | response_prompt
    | llm
    | StrOutputParser()
)

# Streamlit App Interface
def main():
    st.title("SQL Chatbot")
    st.write("Ask questions about the Chinook database in natural language.")

    # Input field for user question
    question = st.text_input("Enter your question:")

    if question:
        # Generate response using the full chain
        response = full_chain.invoke({"question": question})
        st.write("Response:")
        st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()