# Använder officiell python - image som körmiljö
FROM python:3.11-slim

# Sätt en arbetsmapp i containern
WORKDIR /app

# Kopiera över requirements.txt och installera beroenden
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera över hela projektet
COPY . .

# Projektet körs på port 3000
EXPOSE 3000

# Kör appen
CMD [ "python", "main.py" ]



