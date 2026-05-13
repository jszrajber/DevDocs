from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.deps import get_db
from .config.logger import setup_logging, logger
from .schemas.request import QuestionRequest
from backend.graph.graph import graph_app
from fastapi.responses import StreamingResponse
from backend.app.models.conversation import Conversation
from sqlalchemy import select
from langchain.messages import HumanMessage, AIMessage
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
import re

setup_logging()  # Logger starts with an app


app = FastAPI()

origins = [
    "http://localhost:3000",  # Dev port Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    thread_id = uuid.UUID(req.thread_id) if req.thread_id else uuid.uuid4()

    question = req.question
    full_answer = []    # Collecting chunks for db
    confidence_value = "unknown"

    result = await db.execute(
        select(Conversation)
        .where(Conversation.thread_id == thread_id)
        .order_by(Conversation.created_at)
    )

    history = result.scalars().all()

    chat_history = []
    for record in history:
        chat_history.append(HumanMessage(record.question))
        chat_history.append(AIMessage(record.answer))

    # async because of async events inside
    async def generate():
        nonlocal confidence_value

        # Iteration must bye async
        async for event in graph_app.astream_events({    # Method gets every action in graph as dicts
            "question": question,
            "chat_history": chat_history
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

        answer_text = "".join(full_answer)
        # re.sub changes pattern to empty string
        # re.DOTALL fits chars to new line
        answer_text = re.sub(r'\{.*?"confidence".*?\}', '', answer_text, flags=re.DOTALL).strip()

        response = Conversation(
            thread_id=thread_id,
            question=question,
            answer=answer_text,
            confidence=confidence_value
        )

        db.add(response)
        await db.commit()

        logger.info(f"Record for question: {question} was saved in database")

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"X-Thread-Id": str(thread_id)}     # Adding thread_id to header
        )
