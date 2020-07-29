Dockerfile
```
FROM python:3.7.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
```
docker-compose.yml
```
version: '3'

services: # each service is a `docker container`
  web: # sudo docker-compose run web python manage.py shell #DJANGO Container
       # docker-compose run -p 8002:8002  web python -m uvicorn main:app --reload --host "0.0.0.0" --port 8002
    restart: always
    build: .
    command: python -m uvicorn main:app --reload --host "0.0.0.0" --port 8002 --reload   #gunicorn -k uvicorn.workers.UvicornWorker main:app 
    volumes:
      - .:/code
    ports:
      - "8002:8002"

# Note: `Dockerfile` build is also taken care by `docker-compose up`. 
#        Just copy paste the respective Dockerfile
```