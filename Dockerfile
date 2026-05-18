FROM python:3.11.15
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD alembic upgrade head; python src/main.py