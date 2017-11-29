FROM python:3.6.3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY src src

CMD python main.py