# Base image com Python 3.13
FROM python:3.13-slim

# Evita buffers de saída
ENV PYTHONUNBUFFERED 1

# Cria pasta da aplicação
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copia arquivos do projeto
COPY pyproject.toml poetry.lock* /app/

# Instala dependências via Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copia o restante do código
COPY . /app/

# Expõe a porta
EXPOSE 8000

# Comando padrão para rodar o Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]