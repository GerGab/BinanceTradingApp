# this version of linux makes pandas and numpy installation possible
FROM python:slim-buster

WORKDIR /app
#install dependencies:
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

#Copy all
COPY . .

#Run the application:
ENTRYPOINT [ "gunicorn","-b :8080","-w 1","run:app" ]