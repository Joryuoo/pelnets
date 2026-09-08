import fitz
import os

pdf_path = r"C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2022\October\2022A_FE_PM_Question.pdf"
out_dir = r"C:\Users\Kyle\Downloads\pelnets\Files"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)

# Each tuple is a range of page indices (start_idx, end_idx inclusive)
questions = {
    1: (2, 5),
    2: (6, 8),
    3: (9, 12),
    4: (13, 17),
    5: (18, 21),
    6: (22, 25),
    7: (26, 32),
    8: (33, 39)
}

for q, (start_idx, end_idx) in questions.items():
    for i, page_idx in enumerate(range(start_idx, end_idx + 1)):
        page = doc[page_idx]
        
        y0 = 40
        y1 = page.rect.height - 40
        
        rect = fitz.Rect(40, y0, page.rect.width - 40, y1)
        pix = page.get_pixmap(clip=rect, dpi=200)
        out_path = os.path.join(out_dir, f"2022A_FE-B_Q{q}_p{i+1}.png")
        pix.save(out_path)
        print(f"Saved {out_path}")
