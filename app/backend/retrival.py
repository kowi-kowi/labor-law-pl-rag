import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ---- FAISS + chunks ----
path = "../data/" # adjust path as needed
chunks = json.load(open(path + "meta.json", "r", encoding="utf-8"))
index = faiss.read_index(path + "index.faiss")
embedder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, docs, top_k=5):
    pairs = [(query, d["text"]) for d in docs]
    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(docs, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [d for d, s in ranked[:top_k]]

def retrieve_context(query, k=5):
    emb = embedder.encode([query])
    D, I = index.search(np.array(emb), 20)

    candidates = [
        chunks[i] for i in I[0]
        if chunks[i].get("artykul")
    ]

    return rerank(query, candidates, top_k=k)

# ---- HuggingFace LLM ----
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_4bit=True
)

def ask_llm(query, context):
    prompt = f"""
Odpowiadaj tylko na podstawie dostarczonego kontekstu.
Jeżeli brak informacji – napisz wprost.
Cytuj artykuły jeśli to możliwe.

Kontekst:
{context}

Pytanie:
{query}

Odpowiedź:
"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=400, temperature=0.2)
    return tokenizer.decode(output[0], skip_special_tokens=True)