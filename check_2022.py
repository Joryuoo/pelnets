import fitz

pdf_path = r"C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2022\October\2022A_FE_PM_Question.pdf"
try:
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")

    for i in range(len(doc)):
        text = doc[i].get_text("text")
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if lines:
            for line in lines:
                # To match "Q1.", "Q11.", etc.
                if line.startswith("Q") and len(line) > 1 and line[1].isdigit() and "." in line[:5]:
                    print(f"Page {i+1} (index {i}): {line[:30].encode('ascii', 'ignore').decode('ascii')}")
except Exception as e:
    print(f"Error: {e}")
