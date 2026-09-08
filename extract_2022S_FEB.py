import fitz
import os

pdf_path = r"C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2022\April\2022S_FE_PM_Question.pdf"
out_dir = r"C:\Users\Kyle\Downloads\pelnets\Files"

doc = fitz.open(pdf_path)

# Each tuple is a range of page indices (start_idx, end_idx inclusive)
questions = {
    1: (2, 7),
    2: (8, 11),
    3: (12, 16),
    4: (17, 21),
    5: (22, 26),
    6: (27, 31),
    7: (32, 38),
    8: (39, 46)
}

for q, (start_idx, end_idx) in questions.items():
    for i, page_idx in enumerate(range(start_idx, end_idx + 1)):
        page = doc[page_idx]
        
        y0 = 40
        y1 = page.rect.height - 40
        
        rect = fitz.Rect(40, y0, page.rect.width - 40, y1)
        pix = page.get_pixmap(clip=rect, dpi=200)
        out_path = os.path.join(out_dir, f"2022S_FE-B_Q{q}_p{i+1}.png")
        pix.save(out_path)
        print(f"Saved {out_path}")
