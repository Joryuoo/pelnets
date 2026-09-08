import fitz

pdf_path = r"C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2022\April\2022S_FE_PM_Question.pdf"
doc = fitz.open(pdf_path)

for i in range(len(doc)):
    text = doc[i].get_text("text")
    if "Q8" in text or "Question 8" in text:
        print(f"Found Q8 on Page {i+1}")
