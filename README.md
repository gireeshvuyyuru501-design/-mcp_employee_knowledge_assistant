# MCP Employee Knowledge Assistant

This is a small MCP project for the AI Bootcamp.

## Project Goal

Connect an AI assistant to an external source called `employees.csv`.

Without MCP, the AI only knows what the user types.

With MCP, the AI can call tools that read live data from an external file.

## External Source

`employees.csv`

The file contains employee data:

- id
- name
- department
- email
- salary

## MCP Flow

```text
AI Assistant
   ↓
MCP Server
   ↓
employees.csv
   ↓
Answer returned to AI
```

## Tools Provided

| Tool | What it does |
|---|---|
| `list_employees` | Shows all employees |
| `find_employee` | Finds an employee by name |
| `search_department` | Shows employees in one department |
| `get_employee_email` | Gets an employee email address |

## Example Questions

Ask the AI assistant:

```text
List all employees.
Find employee Ravi.
Show employees in IT department.
What is Asha's email?
```

## Install

```bash
pip install mcp
```

## Run

```bash
python server.py
```

## Why This Project Is Useful

This project shows when MCP is needed.

Use normal AI for thinking and explanation.

Use MCP when AI must connect to external data, tools, or systems.
