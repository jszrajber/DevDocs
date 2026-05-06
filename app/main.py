from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from .config.logger import setup_logging, logger
from .schemas.request import QuestionRequest
from graph.graph import graph_app
from fastapi.responses import StreamingResponse
from app.models.conversation import Conversation
import json

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
async def get_response(
    req: QuestionRequest,
    db: AsyncSession = Depends(get_db)
):
    question = req.question
    full_answer = [] # Collecting chunks for db
    confidence_value = "unknown"

    # async because of async events inside
    async def generate():
        nonlocal confidence_value
        
        # Iteration must bye async
        async for event in graph_app.astream_events({    # Method gets every action in graph as dicts
            "question": question
        }, version="v2"):   # v2 gives more info, new version of event formattting

            if event['event'] == "on_chat_model_stream":
                if event['metadata']['langgraph_node'] == "answer":
                    chunk = event["data"]["chunk"]
                    if chunk:
                        full_answer.append(chunk.content)
                        yield chunk.content
                        
            if event['event'] == "on_chat_model_end":
                output = event['data'].get("output").content
                if output and output.strip():
                    try:
                        confidence_value = json.loads(output)["confidence"]
                    except (json.JSONDecodeError, KeyError):
                        confidence_value = "unknown"
                 
        response = Conversation(
            question=question,
            answer="".join(full_answer),
            confidence=confidence_value
        )
        
        
        db.add(response)
        await db.commit()
        
        logger.info(f"Record for question: {question} was saved in database")
        
    return StreamingResponse(generate(), media_type="text/event-stream")