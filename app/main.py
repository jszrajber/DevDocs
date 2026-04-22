from fastapi import FastAPI, HTTPException
from .config.logger import setup_logging, logger
from .schemas.request import QuestionRequest
from graph.graph import graph_app

setup_logging()  # Logger starts with an app


app = FastAPI()

logger.info("Application startup: Logging configured successfully")


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/chat")
async def get_response(req: QuestionRequest):
    result = await graph_app.ainvoke({
        "question": req.question
    })

    answer = result.get("answer")

    if answer:
        return {"answer": answer}

    raise HTTPException(status_code=400, detail="Answer was not generated")
    