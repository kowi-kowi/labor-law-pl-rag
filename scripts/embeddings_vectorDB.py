from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

chunks = json.load(open("./data/chunks.json","r", encoding="utf-8"))

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

embeddings = model.encode(chunks)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

faiss.write_index(index, "./data/index.faiss")