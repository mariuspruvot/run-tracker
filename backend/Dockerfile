# Base Image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install the project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Install zsh
RUN apt-get install -y zsh

# Install Oh My Zsh
RUN sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"


# Copy the rest of the application
COPY . .

# Set the command to run the application
CMD ["poetry", "run", "python", "backend/main.py"]
