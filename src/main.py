import logging

from fastapi import FastAPI

import schema
from extractor import get_extractor


logger = logging.getLogger(__file__)
app = FastAPI()


@app.get('/')
def liveness():
    return 'Hello world !'


@app.post('/extract')
def extract(req: schema.Extraction.Request) -> schema.Extraction.Response:
    # identify extractor
    extractor = get_extractor(req.model)
    print(f"{extractor = }")
    return schema.Extraction.Response(
        results=[
            schema.Extraction.Response.ExtractionResult(
                task=task,
                attributes={
                    attr: extractor.extract(task.full_text(), attr)
                    for attr in task.fields_to_extract
                }
            )
            for task in req.tasks
        ]
    )
