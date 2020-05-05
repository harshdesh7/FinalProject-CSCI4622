FROM python:3

WORKDIR /app

COPY /src /app

WORKDIR /app

EXPOSE 8080

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["classifier.py"]


