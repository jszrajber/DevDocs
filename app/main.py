from fastapi import FastAPI, HTTPException
from .config.logger import setup_logging, logger
from .schemas.request import QuestionRequest
from graph.graph import graph_app
from fastapi.responses import StreamingResponse

setup_logging()  # Logger starts with an app


app = FastAPI()

logger.info("Application startup: Logging configured successfully")


@app.get("/")
def health_check():
    return {"status": "ok"}


# @app.post("/chat")
# async def get_response(req: QuestionRequest):
#     result = await graph_app.ainvoke({
#         "question": req.question
#     })

#     answer = result.get("answer")

#     if answer:
#         return {"answer": answer}

#     raise HTTPException(status_code=400, detail="Answer was not generated")


@app.post("/chat")
async def get_response(req: QuestionRequest):

    # async because of async events inside
    async def generate():
        # Iteration must bye async
        async for event in graph_app.astream_events({    # Method gets every action in graph as dicts
            "question": req.question
        }, version="v2"):   # v2 gives more info, new version of event formattting

            if event['event'] == "on_chat_model_stream":
                if event['metadata']['langgraph_node'] == "answer":
                    chunk = event["data"]["chunk"]
                    if chunk:
                        yield chunk.content

    return StreamingResponse(generate(), media_type="text/event-stream")