# 🤖 SQL Chatbot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688.svg">
  <img src="https://img.shields.io/badge/Database-MySQL%20%7C%20SQL%20Server-orange.svg">
  <img src="https://img.shields.io/badge/Status-Active-success.svg">
  <img src="https://img.shields.io/github/license/Krishiv1903/sql_Chatbot">
</p>

A conversational AI chatbot built using **FastAPI** that enables users to interact with SQL databases using natural language. The application converts user queries into SQL, retrieves relevant information, and provides conversational responses through an intuitive web interface.

---

## ✨ Features

- 💬 Natural language chatbot interface
- 🗄️ SQL database querying
- ⚡ FastAPI backend
- 🤖 LLM-assisted query parsing
- 👨‍⚕️ Domain-specific Doctor Agent
- 🔌 MCP server integration
- 🎨 Simple web-based chat interface
- 🧩 Modular and extensible architecture

---

# 📁 Project Structure

```text
sql_Chatbot/
│
├── app/
│   ├── chatbot/
│   │   ├── chatbot.py          # Main chatbot orchestration
│   │   ├── doctor_agent.py     # Doctor-specific agent
│   │   └── llm_parser.py       # LLM response parsing
│   │
│   ├── db/
│   │   └── db.py               # Database connection & queries
│   │
│   ├── services/
│   │   ├── doctor_service.py   # Domain logic
│   │   └── service.py          # Shared services
│   │
│   ├── mcp/
│   │   └── server.py           # MCP server
│   │
│   └── main.py                 # FastAPI entry point
│
├── static/
│   ├── index.css
│   └── index.js
│
├── templates/
│   └── chat.html
│
├── requirements.txt
└── README.md
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Programming Language |
| FastAPI | Backend Framework |
| MySQL Connector | MySQL Database |
| pyodbc | SQL Server Connectivity |
| HTML/CSS/JavaScript | Frontend UI |
| MCP | Tool Integration |

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Krishiv1903/sql_Chatbot.git
cd sql_Chatbot
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configuration

Before running the application, configure your database connection inside:

```text
app/db/db.py
```

Update:

- Database Server
- Username
- Password
- Database Name
- Driver (if required)

---

# ▶️ Running the Application

```bash
python app/main.py
```

Once the server starts, open your browser and navigate to:

```
http://127.0.0.1:8000
```

---

# 💡 How It Works

```text
User
   │
   ▼
Chat UI
   │
   ▼
FastAPI Backend
   │
   ▼
LLM Parser
   │
   ▼
SQL Query Generation
   │
   ▼
Database
   │
   ▼
Results
   │
   ▼
Conversational Response
```

---

# 📦 Dependencies

Main packages used:

```text
FastAPI
mysql-connector-python
pyodbc
uvicorn
jinja2
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# 📌 Future Improvements

- ✅ Authentication
- ✅ Chat history
- ✅ Multi-database support
- ✅ Streaming responses
- ✅ Docker support
- ✅ Role-based agents
- ✅ Better prompt engineering
- ✅ Query visualization

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push the branch

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Krishiv Goyal**

GitHub: **https://github.com/Krishiv1903**