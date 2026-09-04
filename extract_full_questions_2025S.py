import fitz
import os

pdf_path = r"C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2025\April\2025S_FE-A_Questions.pdf"
out_dir = r"C:\Users\Kyle\Downloads\pelnets\Files"
os.makedirs(out_dir, exist_ok=True)
doc = fitz.open(pdf_path)

questions = {
    4: (4, "Q4.", None),
    5: (5, "Q5.", "Q6."),
    6: (5, "Q6.", None),
    7: (6, "Q7.", "Q8."),
    10: (7, "Q10.", "Q11."),
    13: (8, "Q13.", "Q14."),
    14: (8, "Q14.", None),
    17: (9, "Q17.", "Q18."),
    20: (10, "Q20.", None),
    26: (12, "Q26.", "Q27."),
    35: (15, "Q35.", None),
    37: (16, "Q37.", None),
    55: (22, "Q55.", "Q56."),
    58: (23, "Q58.", "Q59.")
}

for q, (page_idx, start, end) in questions.items():
    page = doc[page_idx]
    
    start_inst = page.search_for(start)
    if not start_inst:
        print(f"Start not found for Q{q}")
        continue
        
    y0 = start_inst[0].y0
    
    y1 = page.rect.height - 50
    if end:
        end_inst = page.search_for(end)
        if end_inst:
            y1 = end_inst[0].y0
            
    y0 = max(0, y0 - 10)
    y1 = min(page.rect.height, y1 + 10)
    
    rect = fitz.Rect(40, y0, page.rect.width - 40, y1)
    pix = page.get_pixmap(clip=rect, dpi=200)
    out_path = os.path.join(out_dir, f"2025S_FE-A_Q{q}_full.png")
    pix.save(out_path)
    print(f"Saved {out_path}")
