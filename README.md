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

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Install the Python libraries required for the project from the requirements.txt file 

```bash
pip install -r requirements.txt
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
