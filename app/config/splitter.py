from langchain_text_splitters import RecursiveCharacterTextSplitter
from docs_source.test_source import text

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
