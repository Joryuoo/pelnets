import fitz
import json
import re

pdf_path = r"C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2021\October\2021A_FE_AM_Questions.pdf"
doc = fitz.open(pdf_path)

questions = {}

for page_num in range(doc.page_count):
    page = doc[page_num]
    blocks = page.get_text("blocks")
    
    current_q = None
    current_text = ""
    
    for b in blocks:
        text = b[4]
        # Match Q1., Q2., etc.
        m = re.match(r'^Q(\d+)\.', text.strip())
        if m:
            if current_q:
                questions[current_q] = current_text.strip()
            current_q = int(m.group(1))
            current_text = text
        elif current_q:
            current_text += "\n" + text
            
    if current_q:
        if current_q in questions:
            questions[current_q] += "\n" + current_text.strip()
        else:
            questions[current_q] = current_text.strip()

print(f"Extracted {len(questions)} questions text.")
with open(r"C:\Users\Kyle\Downloads\pelnets\2021A_questions_text.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)
