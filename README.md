# CS356-Group-3-Backend
Group project module for CS356

## 🏗️ Tech Stack

- **Python 3.10+**
- **[FastAPI](https://fastapi.tiangolo.com/)** – API framework
- **[Poetry](https://python-poetry.org/)** – Dependency & project management
- **Uvicorn** – ASGI server

## 🚀 Getting Started

### Prerequisites

Install [Poetry](https://python-poetry.org/docs/#installation):
Install [SQL Model](https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Installation

```bash
poetry install
```

### Run the API

```bash
poetry run uvicorn app.main:app --reload
```

- Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Run the Database

TODO - combine with main api

Change Directory to app/database
```command
fastapi dev set_up_database.py
```