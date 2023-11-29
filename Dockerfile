FROM python:3.12

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY src .

EXPOSE 8080

CMD python -m uvicorn --host 0.0.0.0 --port 8080 main:app
