FROM python:3.12-slim

WORKDIR /app

# System deps + OpenCV runtime
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Install Python deps
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# Copy source
COPY . /app

# Expose and run
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]