# Import necessary libraries

# This file accepts questions in natural language, provides responses in natural language, and also generates appropriate visualizations (such as line charts, bar graphs, or pie charts) based on the question.

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import re
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Load environment variables
load_dotenv()

# Initialize the database connection
db_url = "mysql+mysqlconnector://root:1234@localhost:3306/Chinook"
db = SQLDatabase.from_uri(db_url)

# Configure Azure OpenAI settings
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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

# Function to execute SQL queries and return a DataFrame
def run_query(query):
    try:
        engine = create_engine(db_url)
        df = pd.read_sql(query.strip(), engine)
        return df
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

# Define the prompt template for suggesting visualizations
visualization_template = """
You are an AI assistant that recommends appropriate data visualizations based on the user's question and the generated SQL query. Analyze the question and query to determine the data's nature (e.g., time series, categorical, relational, hierarchical, geographical) and suggest the most suitable chart type. Follow these guidelines:

- For trends over time (e.g., dates, months, years), suggest a "line" chart.
- For comparisons across categories (e.g., counts by group), suggest a "bar" chart unless explicitly requested otherwise.
- For relationships between two numerical variables, suggest a "scatter" chart.
- For proportional contributions to a whole (e.g., percentages by category), suggest a "pie" or "donut" chart.
- For distributions of a single numerical variable, suggest a "histogram" or "box" chart.
- For hierarchical or nested data, suggest a "treemap" or "sunburst" chart.
- For geographical data, suggest a "map" or "choropleth" chart.
- For single aggregated values (e.g., total count), suggest a "bar" chart with a single bar, unless another type is explicitly requested.
- For multi-dimensional comparisons, suggest a "heatmap" or "grouped bar" chart.
- If no visualization is appropriate, use "none".

Output your suggestion in JSON format with the following keys:
- "chart_type": the type of chart, e.g., "line", "bar", "scatter", "pie", "histogram", "box", "treemap", "sunburst", "map", "heatmap", or "none"
- "x_axis": the column name for categories (e.g., "GenreName" for pie charts, "Month" for time), or null if not applicable
- "y_axis": the column name for values (e.g., "PercentageOfTotalSales" for pie charts, "Sales" for bar charts), or null if not applicable
- "other": any additional info (e.g., "group by Genre", "show percentages"), or null if not needed

Question: {question}

SQL Query: {query}

Suggested Visualization (JSON):
"""
visualization_prompt = ChatPromptTemplate.from_template(visualization_template)

# Initialize the LLM (Azure OpenAI)
llm = AzureChatOpenAI(
    deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
    temperature=0,
    cache=False,
    openai_api_key=OPENAI_API_KEY,
    openai_api_version=OPENAI_API_VERSION,
)

# Define the visualization response schema
viz_response_schema = [
    ResponseSchema(
        name="chart_type",
        description="The type of chart, e.g., 'line', 'bar', 'scatter', 'pie', 'histogram', 'box', 'treemap', 'sunburst', 'map', 'choropleth', 'heatmap', or 'none'."
    ),
    ResponseSchema(
        name="x_axis",
        description="The column name or label for the x-axis, or null if not applicable (e.g., pie charts)."
    ),
    ResponseSchema(
        name="y_axis",
        description="The column name or label for the y-axis, or null if not applicable (e.g., pie charts)."
    ),
    ResponseSchema(
        name="other",
        description="Any additional relevant information, or null if not needed.",
        default=None
    ),
]
viz_parser = StructuredOutputParser.from_response_schemas(viz_response_schema)

# Create the SQL generation chain
sql_chain = (
    RunnablePassthrough.assign(schema=lambda x: get_schema())
    | sql_prompt
    | llm.bind(stop=["\n SQL Result:"])
    | StrOutputParser()
    | clean_sql_query
)

# Create the visualization suggestion chain
viz_chain = (
    RunnablePassthrough.assign(schema=lambda x: get_schema())
    | visualization_prompt
    | llm
    | viz_parser
)

# Create the full chain for generating natural language responses and visualizations
full_chain = (
    RunnablePassthrough.assign(query=sql_chain)
    .assign(viz_suggestion=viz_chain)
    .assign(df_response=lambda x: run_query(x["query"]))
    .assign(schema=lambda x: get_schema())
    .assign(
        text_response=lambda x: (response_prompt | llm | StrOutputParser()).invoke({
            "question": x["question"],
            "query": x["query"],
            "response": x["df_response"].to_string() if isinstance(x["df_response"], pd.DataFrame) else x["df_response"],
            "schema": x["schema"]
        })
    )
)

# Function to generate Plotly visualization based on suggestion
def generate_visualization(df, viz_suggestion):
    if not isinstance(df, pd.DataFrame) or viz_suggestion["chart_type"] == "none":
        return None
    chart_type = viz_suggestion["chart_type"]
    x_axis = viz_suggestion["x_axis"]
    y_axis = viz_suggestion["y_axis"]
    other = viz_suggestion["other"]

    # Infer x_axis and y_axis for pie charts if not provided
    if chart_type == "pie":
        if x_axis is None or y_axis is None:
            # Assume first column is categories, second is values
            if len(df.columns) >= 2:
                x_axis = df.columns[0]  # e.g., 'GenreName'
                y_axis = df.columns[1]  # e.g., 'PercentageOfTotalSales'
            else:
                return None
        if x_axis in df.columns and y_axis in df.columns:
            fig = px.pie(df, names=x_axis, values=y_axis, title=f"Distribution of {y_axis} by {x_axis}")
            return fig

    # Handle single-value cases (e.g., total counts)
    if len(df) == 1 and chart_type in ["bar", "line", "scatter"]:
        y_value = df.iloc[0][0] if df.columns[0] != x_axis else df.iloc[0][1]
        plot_df = pd.DataFrame({x_axis: [x_axis], y_axis: [y_value]})
        if chart_type == "bar":
            fig = px.bar(plot_df, x=x_axis, y=y_axis, title=f"{y_axis} of {x_axis}", text=plot_df[y_axis])
            fig.update_traces(textposition='auto')
            return fig
        elif chart_type == "line":
            fig = px.line(plot_df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
            return fig
        elif chart_type == "scatter":
            fig = px.scatter(plot_df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
            return fig

    # Handle multi-row cases
    if chart_type == "line" and x_axis in df.columns and y_axis in df.columns:
        fig = px.line(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
        return fig
    elif chart_type == "bar" and x_axis in df.columns and y_axis in df.columns:
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
        return fig
    elif chart_type == "scatter" and x_axis in df.columns and y_axis in df.columns:
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
        return fig
    elif chart_type == "histogram" and x_axis in df.columns:
        fig = px.histogram(df, x=x_axis, title=f"Distribution of {x_axis}")
        return fig
    else:
        st.write(f"Debug: Chart type {chart_type}, x_axis {x_axis}, y_axis {y_axis}, df columns {df.columns}")
        return None

# Streamlit App Interface
def main():
    st.title("SQL Chatbot with Dynamic Visualization")
    st.write("Ask questions about the Chinook database in natural language.")

    # Input field for user question
    question = st.text_input("Enter your question:")

    if question:
        # Generate response and visualization using the full chain
        result = full_chain.invoke({"question": question})
        
        # Display natural language response
        st.write("Response:")
        st.write(result["text_response"])
        
        # Generate and display visualization if applicable
        viz_fig = generate_visualization(result["df_response"], result["viz_suggestion"])
        if viz_fig:
            st.write("Visualization:")
            st.plotly_chart(viz_fig)
        else:
            st.write("No suitable visualization generated.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
