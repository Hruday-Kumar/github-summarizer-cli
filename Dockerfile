# Dockerfile

# 1. Start FROM a "base" container that already has Python
FROM python:3.10-slim

# 2. Set the "working directory" inside the container
WORKDIR /app

# 3. COPY your "ingredients list" into the container
COPY requirements.txt .

# 4. RUN the command to install all your libraries
RUN pip install -r requirements.txt

# 5. COPY all your application code (summarize.py and .env)
COPY . .

# 6. This is the default CMD (command) to run when the container starts
# We are setting it up to wait for a URL to be provided.
ENTRYPOINT ["python", "summarize.py"]