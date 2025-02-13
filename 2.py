from typing import Annotated
from fastapi import FastAPI, Query , Path

app = FastAPI()

@app.get('/items/{item_id}')
async def read_items(
    *,
    item_id : Annotated[int , Path(title='The id of the item ', ge=0 , le=1000)],
    q: str,
    size: Annotated[float , Query(gt =0 , le=10.5)]
):
    results = {"item_id" : item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results
