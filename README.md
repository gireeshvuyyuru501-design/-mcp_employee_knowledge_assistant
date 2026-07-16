# 🚀 Enterprise Employee Knowledge Assistant (MCP)

> Production-ready Enterprise Employee Knowledge Assistant built using **Model Context Protocol (MCP)**, **FastAPI**, **LangGraph**, **Python**, and **PostgreSQL** for intelligent enterprise knowledge retrieval and AI agent orchestration.

---

# 📖 Overview

The Enterprise Employee Knowledge Assistant is an AI-powered platform that enables employees to search, retrieve, and manage enterprise knowledge through conversational AI.

The application combines **Model Context Protocol (MCP)**, **LangGraph**, **FastAPI**, and **PostgreSQL** to provide secure, scalable, and production-ready AI services.

---

# 🎯 Business Problem

Large organizations struggle to provide employees with instant access to company knowledge, policies, and employee information.

Traditional search systems are:

- Slow
- Keyword-based
- Difficult to maintain
- Unable to understand natural language

---

# 💡 Solution

This application provides an AI-powered enterprise assistant capable of:

- Searching employee information
- Natural language knowledge retrieval
- REST API integration
- Enterprise CRUD operations
- AI-powered responses using MCP architecture
- Modular backend services

---

# 🏗️ Architecture

```
                        User
                          │
                          ▼
                   FastAPI REST API
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   Authentication      MCP Server      LangGraph Agents
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                    Business Logic
                          │
                          ▼
                    PostgreSQL Database
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- JWT Authentication

## AI

- Model Context Protocol (MCP)
- FastMCP
- LangGraph
- LangChain
- Claude API

## DevOps

- Docker
- GitHub Actions
- CI/CD

---

# ✨ Features

✅ Employee Search

✅ Department Filtering

✅ CRUD Operations

✅ REST APIs

✅ AI Knowledge Assistant

✅ MCP Integration

✅ LangGraph Agent Workflow

✅ Authentication

✅ Pydantic Validation

✅ PostgreSQL Database

✅ Docker Support

---

# 📂 Project Structure

```
backend/
│
├── api/
├── agents/
├── database/
├── models/
├── schemas/
├── services/
├── config/
├── tests/
│
frontend/
│
README.md
```

---

# ⚙️ Installation

```bash
git clone https://github.com/gireeshvuyyuru501-design/mcp_employee_knowledge_assistant.git

cd mcp_employee_knowledge_assistant

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|----------|------------------------|-----------------------------|
| GET | / | Health Check |
| GET | /employees | List Employees |
| GET | /employees/{id} | Employee Details |
| POST | /employees | Create Employee |
| PUT | /employees/{id} | Update Employee |
| DELETE | /employees/{id} | Delete Employee |
| POST | /chat | AI Chat Assistant |

---

# 📊 Project Highlights

- Built production-ready MCP architecture
- Enterprise REST APIs using FastAPI
- LangGraph AI workflow orchestration
- PostgreSQL backend
- Secure authentication
- Modular architecture
- Scalable API design
- Docker-ready deployment

---

# 🚀 Future Enhancements

- Kubernetes Deployment
- Redis Caching
- Streaming AI Responses
- Vector Database Integration
- LangSmith Observability
- AWS Deployment
- Role-Based Access Control
- Monitoring Dashboard

---

# 👨‍💻 Author

**Girish V**

AI/ML Engineer | Generative AI | Agentic AI

📧 Email: girishsap45@gmail.com

💼 LinkedIn:
https://www.linkedin.com/in/girish-genai-engineer

💻 GitHub:
https://github.com/gireeshvuyyuru501-design

---

# ⭐ If you found this project useful

Please ⭐ Star this repository.
