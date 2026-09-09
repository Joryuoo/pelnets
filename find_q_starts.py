import fitz
import json

doc = fitz.open(r'C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2021\April\2021S_FE_PM_Question.pdf')

q_starts = {}
for i in range(doc.page_count):
    text = doc[i].get_text()
    if text:
        import re
        m = re.search(r'Q(\d+)\.\s', text)
        if m:
            q = int(m.group(1))
            if q not in q_starts:
                q_starts[q] = i

print(q_starts)
