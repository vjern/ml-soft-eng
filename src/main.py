import logging

from fastapi import FastAPI

from schema import PostExtract, ExtractionResult
from extractor import get_extractor


logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__file__)
app = FastAPI()


@app.get('/')
def liveness():
    return 'llm-extractor v0.1.0'


@app.post('/extract')
def post_extract(req: PostExtract.Request) -> PostExtract.Response:
    # identify extractor
    extractor = get_extractor(req.model)
    logger.info(f"{extractor = }")
    return PostExtract.Response(
        results=[
            ExtractionResult(
                product_description=task.product_description,
                fields={
                    field_id: extractor.extract(task.product_description, field_id)
                    for field_id in task.fields_to_extract
                }
            )
            for task in req.tasks
        ]
    )
