FROM python:3.8-slim-buster
WORKDIR /code
COPY ./Blob/Application/backend/requirements.txt /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./Blob/Application/backend /code
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "80"]
