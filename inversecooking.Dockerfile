FROM python:3.6
WORKDIR /inversecooking

COPY requirements.txt /inversecooking
RUN pip install -r requirements.txt
COPY inverse-cooking /inversecooking

CMD ["python", "src/inversecooking-api.py"]