import fitz
import os

pdf_path = r"C:\Users\Kyle\Downloads\pelnets\Exam_Q&A\2021\October\2021A_FE_AM_Questions.pdf"
out_dir = r"C:\Users\Kyle\Downloads\pelnets\Files"

os.makedirs(out_dir, exist_ok=True)
doc = fitz.open(pdf_path)

# Build a list of (q_num, page_num, y_coord)
questions = []
for page_num in range(doc.page_count):
    page = doc[page_num]
    text_instances = []
    # Search for Q1. through Q80.
    for i in range(1, 81):
        q_text = f"Q{i}."
        rects = page.search_for(q_text)
        for r in rects:
            # Check if it's actually just Q{i}. and not Q10. matching Q1.
            # PyMuPDF search_for is usually exact or substring, but let's be careful.
            # We'll just assume the first match that is on the left side is it.
            if r.x0 < 100:  # Questions usually start on the left margin
                text_instances.append((i, r.y0))
    
    text_instances.sort(key=lambda x: x[1])
    
    for idx, (q_num, y0) in enumerate(text_instances):
        y0_clip = max(0, y0 - 10)
        
        if idx + 1 < len(text_instances):
            y1_clip = text_instances[idx+1][1] - 10
        else:
            y1_clip = page.rect.y1 - 40
            
        clip = fitz.Rect(0, y0_clip, page.rect.x1, y1_clip)
        pix = page.get_pixmap(clip=clip, dpi=150)
        
        out_path = os.path.join(out_dir, f"2021A_FE_AM_Q{q_num}_full.png")
        pix.save(out_path)
        print(f"Saved {out_path}")

print("Done cropping.")
