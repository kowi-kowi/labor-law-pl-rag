import pdfplumber

text = ""
with pdfplumber.open("./data/raw/D2025000027701.pdf") as pdf:
    for page in pdf.pages:
        text += page.extract_text() + "\n"

open("./data/processed/kodeks_pracy.txt", "w", encoding="utf-8").write(text)