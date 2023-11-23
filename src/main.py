from fastapi import FastAPI

from .schema import ExtractRequest


app = FastAPI()


@app.get('/')
def liveness():
    return 'Hello world !'


@app.post('/extract')
def extract(body: ExtractRequest):
    print(body)
