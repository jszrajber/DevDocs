from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from app.config.settings import settings

checkpointer = AsyncPostgresSaver.from_conn_string(settings.POSTGRESSAVER_URL)