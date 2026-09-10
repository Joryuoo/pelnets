import sys
import os
import json
import re
import fitz  # PyMuPDF

def process_am_pdf(pdf_path, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    doc = fitz.open(pdf_path)
    base_name = os.path.basename(pdf_path).replace("_Question.pdf", "")
    print(f"Processing {base_name} AM exam...")

    # Find the positions of Q1 to Q81 (81 is the end of Q80)
    q_positions = {}
    
    for p in range(doc.page_count):
        page = doc[p]
        text = page.get_text()
        
        # Look for "Q[1-80]." or "Q[1-80] " 
        # (Handling the edge case where the period is missing, e.g. "Q35 ")
        for q in range(1, 81):
            if q in q_positions:
                continue
                
            # Try to find exactly "Q1." or "Q1 "
            rects = page.search_for(f"Q{q}.")
            if not rects:
                rects = page.search_for(f"Q{q} ")
                
            if rects:
                # Filter out false positives (must be on the left side of the page generally)
                valid_rects = [r for r in rects if r.x0 < 150]
                if valid_rects:
                    r = valid_rects[0]
                    y0 = max(0, r.y0 - 10)
                    q_positions[q] = (p, y0)
                    print(f"Detected Q{q} on page {p}")

    if not q_positions:
        print("Could not detect any questions automatically. Exiting.")
        return

    # Add a pseudo Q81 to mark the end of Q80
    last_q = max(q_positions.keys())
    last_p = q_positions[last_q][0]
    q_positions[81] = (doc.page_count - 1, doc[doc.page_count - 1].rect.y1)

    extracted_texts = {}

    for q in range(1, 81):
        if q not in q_positions or (q + 1) not in q_positions:
            continue
            
        start_p, start_y = q_positions[q]
        end_p, end_y = q_positions[q + 1]
        
        # 1. Extract Text for the question
        text = ""
        for p in range(start_p, end_p + 1):
            page = doc[p]
            rect = page.rect
            y0 = start_y if p == start_p else 0
            y1 = end_y if p == end_p else rect.y1
            
            clip = fitz.Rect(0, y0, rect.x1, y1)
            text += page.get_text(clip=clip) + "\n"
            
        extracted_texts[str(q)] = text

        # 2. Crop Image for the question
        # If it spans multiple pages, we just save the first page or combine them (usually AM questions fit on one page or two).
        # We will save _p1, _p2 if it spans multiple pages.
        part = 1
        for p in range(start_p, end_p + 1):
            page = doc[p]
            rect = page.rect
            y0 = start_y if p == start_p else 0
            y1 = end_y if p == end_p else rect.y1
            
            if y1 - y0 < 20:
                continue
                
            clip = fitz.Rect(0, y0, rect.x1, y1)
            pix = page.get_pixmap(clip=clip, dpi=150)
            
            # Use full image name like 2020A_FE_AM_Q1_full.png if it's 1 part, else append _p1
            suffix = "_full" if start_p == end_p else f"_p{part}"
            out_path = os.path.join(out_dir, f"{base_name}_Q{q}{suffix}.png")
            pix.save(out_path)
            part += 1

    # Save Text JSON
    json_path = os.path.join(os.path.dirname(pdf_path), f"{base_name}_Questions_Text.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(extracted_texts, f, ensure_ascii=False, indent=2)
    print(f"Extraction complete! Saved {len(extracted_texts)} AM questions.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python global_am_processor.py <path_to_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    out_dir = r"C:\Users\Kyle\Downloads\pelnets\Files"
    process_am_pdf(pdf_path, out_dir)
