import re
import json

PATH_INPUT = "./data/processed/kodeks_pracy.txt"
PATH_OUTPUT = "./data/chunks.json"

with open(PATH_INPUT, "r", encoding="utf-8") as f:
    text = f.read()

# 🔹 twardo wycinamy do "Preambuła (uchylona)" włącznie
cut_marker = "Preambuła (uchylona)"
if cut_marker in text:
    text = text.split(cut_marker, 1)[1]

# 🔹 upewniamy się że startujemy od DZIAŁU PIERWSZEGO
start_marker = "DZIAŁ PIERWSZY"
if start_marker in text:
    text = text[text.index(start_marker):]


# ---------- DALEJ TWÓJ SMART CHUNKER ----------

dzial_regex = r"(DZIAŁ\s+[A-ZŁŻŚĆĘĄÓŃ]+[^\n]*)"
rozdzial_regex = r"(Rozdział\s+[IVXLC]+\s*[^\n]*)"
art_regex = r"(Art\.\s+\d+[^\n]*)"

lines = text.split("\n")

current_dzial = None
current_rozdzial = None
current_art = None
buffer = ""

chunks = []
counter = 0

def save_chunk():
    global buffer, counter, current_dzial, current_rozdzial, current_art
    if buffer.strip():
        chunks.append({
            "id": counter,
            "dzial": current_dzial,
            "rozdzial": current_rozdzial,
            "artykul": current_art,
            "text": buffer.strip()
        })

for line in lines:
    line_strip = line.strip()

    if not line_strip:
        continue

    if re.match(dzial_regex, line_strip):
        save_chunk()
        counter += 1
        current_dzial = line_strip
        current_rozdzial = None
        current_art = None
        buffer = ""
        continue

    if re.match(rozdzial_regex, line_strip):
        save_chunk()
        counter += 1
        current_rozdzial = line_strip
        current_art = None
        buffer = ""
        continue

    if re.match(art_regex, line_strip):
        save_chunk()
        counter += 1
        current_art = line_strip
        buffer = line_strip + "\n"
        continue

    buffer += line_strip + "\n"

save_chunk()

with open(PATH_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print(f"Zapisano {len(chunks)} chunków do {PATH_OUTPUT}")
