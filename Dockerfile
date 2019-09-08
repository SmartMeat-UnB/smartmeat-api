FROM python:3.6
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r ./requirements.txt
COPY smartmeat-api.py /app
COPY . .

CMD ["python", "smartmeat-api.py"]~