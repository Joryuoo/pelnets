import fitz
import os

pdf_path = r"C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2023\April\2023S_FE_PM_Questions.pdf"
out_dir = r"C:\Users\Kyle\Downloads\pelnets\Files"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)

# Each tuple is a range of page indices (start_idx, end_idx inclusive)
questions = {
    1: (2, 5),
    2: (6, 10),
    3: (11, 14),
    4: (15, 18),
    5: (19, 22),
    6: (23, 28),
    7: (29, 36),
    8: (37, 41)
}

for q, (start_idx, end_idx) in questions.items():
    for i, page_idx in enumerate(range(start_idx, end_idx + 1)):
        page = doc[page_idx]
        
        y0 = 40
        y1 = page.rect.height - 40
        
        rect = fitz.Rect(40, y0, page.rect.width - 40, y1)
        pix = page.get_pixmap(clip=rect, dpi=200)
        out_path = os.path.join(out_dir, f"2023S_FE-B_Q{q}_p{i+1}.png")
        pix.save(out_path)
        print(f"Saved {out_path}")

