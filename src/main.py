import logging
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, Request

from schema import PostExtract, ExtractionResult
from extractor import get_extractor, Extractor


DEBUG_HEADER_SHOW_PROMPTS = "X-Debug-Show-Prompts"

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__file__)
app = FastAPI()


@app.get("/")
def liveness():
    return "llm-extractor v0.1.0"


def repack_result(
    extractor: Extractor,
    args: tuple[str, str],
    with_prompt: bool = False,
) -> ExtractionResult:
    """
    Utility function to adapt to ThreadPoolExecutor.map to
    - properly unpack the atomic task args (product desc and id of field to extract)
    - rebuild a result object that includes the prompt if the debug header is provided
    """
    desc, field_id = args
    field_value, prompt = extractor.extract(desc, field_id)
    return ExtractionResult(
        product_description=desc,
        prompt=prompt.split("\n") if with_prompt else None,
        field_value=field_value,
        field_name=field_id,
    )


@app.post("/extract")
def post_extract(req: Request, body: PostExtract.Request) -> PostExtract.Response:
    # Identify the extractor to use
    extractor = get_extractor(body.model)
    logger.info(f"{extractor = }")
    # We allow a debug header to be passed in to also return the generated prompts
    with_prompt = DEBUG_HEADER_SHOW_PROMPTS in req.headers
    split_tasks = (
        (product.description, field_id)
        for product in body.products
        for field_id in product.fields_to_extract
    )

    executor = ThreadPoolExecutor(max_workers=50)
    results = executor.map(
        partial(repack_result, extractor, with_prompt=with_prompt),
        split_tasks,
    )
    return {
        "results": results,
    }
