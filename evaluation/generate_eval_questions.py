import json
import random
import os

META_PATH = "./data/chunks.json"
OUT_PATH = "./evaluation/questions.json"
NUM_QUESTIONS = 10


print("Loading metadata...")
with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

# filtrujemy tylko artykuły (nie działy, rozdziały itp.)
articles = []
for m in meta:
    artykul = m.get("artykul", "")
    try:
        if artykul.startswith("Art."):
            articles.append(m)
    except:
        continue

if len(articles) < NUM_QUESTIONS:
    raise ValueError("Za mało artykułów w bazie, żeby wylosować 10 pytań!")

random.shuffle(articles)
selected = articles[:NUM_QUESTIONS]


def build_question(text, article):
    """
    Bardzo prosty generator pytań na podstawie treści artykułu.
    (heurystyczny ale działa zaskakująco dobrze)
    """

    t = text.lower()

    # kilka prostych „prompt heuristics” dla prawa pracy
    if "pracownik" in t:
        return "Kim jest pracownik według Kodeksu pracy?"
    if "pracodawc" in t:
        return "Kto może być pracodawcą według Kodeksu pracy?"
    if "obowiąz" in t and "pracownik" in t:
        return "Jakie obowiązki ma pracownik według Kodeksu pracy?"
    if "obowiąz" in t and "pracodawc" in t:
        return "Jakie obowiązki ma pracodawca?"
    if "urlop" in t:
        return "Jakie zasady dotyczą urlopu pracownika?"
    if "wynagrodz" in t:
        return "Jakie zasady dotyczą wynagrodzenia za pracę?"
    if "czas pracy" in t:
        return "Jak definiowany jest czas pracy pracownika?"
    if "młodocian" in t:
        return "Jakie zasady dotyczą zatrudniania młodocianych?"
    if "kobiet" in t or "ciąży" in t:
        return "Jakie przepisy chronią kobiety w ciąży w pracy?"

    # fallback gdy nie rozpoznaliśmy tematu
    return f"Czego dotyczy {article} w Kodeksie pracy?"


print("Generating questions...")

dataset = []

for art in selected:
    text = art.get("text", "")
    article_name = art.get("artykul", "NIEZNANY")

    q = {
        "question": build_question(text, article_name),
        "expected_article": article_name,
        "gold_answer": ""  # można uzupełnić później
    }

    dataset.append(q)


os.makedirs("./eval", exist_ok=True)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(f"Saved {len(dataset)} questions to {OUT_PATH}")