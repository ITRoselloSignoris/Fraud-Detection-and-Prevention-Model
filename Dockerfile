FROM python:3.9

RUN apt-get update && apt-get install -y

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn","deployment.main:app","--host=0.0.0.0", "--port=7860"]