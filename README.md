
# SQL Chatbot: AI-Powered Natural Language Querying for Databases

This project demonstrates an **AI-powered chatbot** that allows users to query a SQL database using **natural language questions**. The chatbot leverages **LangChain**, **Azure OpenAI**, and **Streamlit** to generate SQL queries, execute them on the database, and provide natural language responses.

## Features
- Converts natural language questions into SQL queries.
- Executes queries on a MySQL database (`Chinook` dataset).
- Provides human-readable responses in natural language.
- Built with **Azure OpenAI** for advanced NLP capabilities.
- Easy-to-use interface powered by **Streamlit**.

---

## Table of Contents
1. [Setup Instructions](#setup-instructions)
2. [Dependencies](#dependencies)
3. [Environment Variables](#environment-variables)
4. [Database Setup](#database-setup)
5. [Running the App](#running-the-app)
6. [Example Queries](#example-queries)
7. [Directory Structure](#directory-structure)
8. [Contributing](#contributing)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/D-Harshith/Natural-Language-SQL-Chatbot-with-LangChain.git
```

### 2. Install Dependencies
Install the required Python libraries listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory and populate it with your Azure OpenAI credentials:
```plaintext
AZURE_OPENAI_ENDPOINT=<your_azure_endpoint>
AZURE_OPENAI_KEY=<your_azure_key>
AZURE_OPENAI_DEPLOYMENT_NAME=<your_deployment_name>
OPENAI_API_TYPE=azure
OPENAI_API_BASE=<your_api_base>
OPENAI_API_VERSION=<your_api_version>
OPENAI_API_KEY=<your_api_key>
```

> **Note**: Replace placeholders with your actual credentials.

### 4. Database Setup
The project uses the `Chinook` MySQL database. Follow these steps to set it up:

#### Option 1: Import from SQL Dump
1. Install MySQL on your system if not already installed.
2. Import the `Chinook_MySql.sql` file into your MySQL server:
   ```bash
   mysql -u root -p1234 < database/Chinook.sql
   ```

#### Option 2: Use an Existing Database
If you’re using a different database, update the `db_url` variable in `SQL_chatbot.py`:
```python
db_url = "mysql+mysqlconnector://<username>:<password>@<host>:<port>/<database>"
```

---

## Dependencies
The following Python libraries are required:
- `streamlit`
- `langchain`
- `openai`
- `mysql-connector-python`
- `python-dotenv`

You can install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## Environment Variables
Ensure your `.env` file contains the following variables:
```plaintext
AZURE_OPENAI_ENDPOINT=<your_azure_endpoint>
AZURE_OPENAI_KEY=<your_azure_key>
AZURE_OPENAI_DEPLOYMENT_NAME=<your_deployment_name>
OPENAI_API_TYPE=azure
OPENAI_API_BASE=<your_api_base>
OPENAI_API_VERSION=<your_api_version>
OPENAI_API_KEY=<your_api_key>
```

---

## Running the App
To run the app locally, use the following command:
```bash
streamlit run SQL_chatbot.py
```

Once the app starts, open your browser and navigate to `http://localhost:8501`. You will see the chatbot interface where you can ask questions about the database.

---

## Example Queries
Here are some example questions you can ask the chatbot:

1. **"How many artists are there?"**
   - SQL Query: `SELECT COUNT(*) AS NumberOfArtists FROM artist;`
   - Response: `"There are a total of 275 artists in the database."`

2. **"How many employees are there?"**
   - SQL Query: `SELECT COUNT(*) AS NumberOfEmployees FROM employee;`
   - Response: `"There are a total of 8 employees in the database."`

3. **"Print the table names in the database."**
   - Response: `"The database contains the following tables: album, artist, customer, employee, genre, invoice, invoiceline, mediatype, playlist, playlisttrack, and track."`

---

## Directory Structure
```
sql-chatbot/
├── .env                   # Environment variables (DO NOT UPLOAD THIS TO GITHUB)
├── requirements.txt       # List of dependencies
├── README.md              # Documentation for your project
├── SQL_chatbot.py         # Main Python script
├── database/              # Folder for database-related files
│   ├── Chinook.sql        # SQL dump of the Chinook database schema/data
│   └── README.md          # Instructions for setting up the database
└── .gitignore             # Files to exclude from GitHub
```

---

## Contributing
Contributions are welcome! If you’d like to improve this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

---

## License
This project is licensed under the [MIT License](LICENSE).

---
