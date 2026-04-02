# FROM rasa/rasa-sdk:3.9.1

# WORKDIR /app
# COPY . .

# CMD ["rasa-sdk", "run", "--host", "0.0.0.0", "--port", "5055"]

FROM rasa/rasa-sdk:3.9.1

USER root

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

USER 1001

CMD ["start", "--actions", "actions"]