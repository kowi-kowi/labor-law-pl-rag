from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

chunks = json.load(open("./data/chunks.json","r", encoding="utf-8"))

# ⛔️ filtrujemy rekordy bez artykułu lub bez tekstu
clean_chunks = [
    c for c in chunks
    if c.get("text") 
    and isinstance(c.get("text"), str)
    and c.get("text").strip()
    and c.get("artykul") not in [None, "", "null"]
]

print(f"Loaded: {len(chunks)} chunks")
print(f"Using:  {len(clean_chunks)} clean chunks")

texts = [c["text"] for c in clean_chunks]

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

embeddings = model.encode(texts, convert_to_numpy=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))
faiss.write_index(index, "./data/index.faiss")

# zapisujemy spójną metadane bazę pod FAISS
json.dump(clean_chunks, open("./data/meta.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)

print("FAISS index + meta updated")
