FROM python:3.8.1

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

CMD uvicorn --host=0.0.0.0 main:app