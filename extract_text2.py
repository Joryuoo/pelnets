import fitz
import json
import re

pdf_path = r"C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2021\October\2021A_FE_AM_Questions.pdf"
doc = fitz.open(pdf_path)

full_text = ""
for page_num in range(doc.page_count):
    page = doc[page_num]
    full_text += page.get_text() + "\n"

questions = {}

# We know the pattern is roughly "Q1. " to "Q2. ", etc.
# Let's find all indices of Q\d+\.
matches = list(re.finditer(r'\nQ(\d+)\.', "\n" + full_text))

for i in range(len(matches)):
    q_num = int(matches[i].group(1))
    start_idx = matches[i].start()
    if i + 1 < len(matches):
        end_idx = matches[i+1].start()
    else:
        end_idx = len("\n" + full_text)
    
    q_text = ("\n" + full_text)[start_idx:end_idx].strip()
    questions[str(q_num)] = q_text

print(f"Extracted {len(questions)} questions text.")
with open(r"C:\Users\Kyle\Downloads\pelnets\2021A_questions_text.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)
