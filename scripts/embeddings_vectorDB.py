from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

chunks = json.load(open("./data/chunks.json","r", encoding="utf-8"))

texts = [c["text"] for c in chunks]

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

embeddings = model.encode(texts, convert_to_numpy=True)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

faiss.write_index(index, "./data/index.faiss")