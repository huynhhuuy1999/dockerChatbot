FROM python:3.9.6

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN rasa train --force

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug", "--port", "5005"]