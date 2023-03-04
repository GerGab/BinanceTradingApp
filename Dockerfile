FROM python:alpine3.16

WORKDIR /app
#install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

#Copy all
COPY . .

#add curl n lookup
RUN apk add curl
RUN apk add bind-tools
#Run the application:
ENTRYPOINT [ "gunicorn","-b :8080","-w 1","run:app" ]