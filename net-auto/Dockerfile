FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml setup.py requirements.txt ./
RUN pip install --no-cache-dir -e .

COPY . .

ENTRYPOINT ["python", "cli.py"]
