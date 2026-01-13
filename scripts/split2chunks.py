from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

with open("./data/processed/kodeks_pracy.txt", "r", encoding="utf-8") as f:
    text = f.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(text)


json.dump(chunks, open("./data/chunks.json","w", encoding="utf-8"), ensure_ascii=False, indent=2)