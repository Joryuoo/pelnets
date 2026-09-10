import sys
import os
import json
import re
import fitz  # PyMuPDF

def get_tight_clip(page, y_start, y_end):
    blocks = page.get_text("blocks")
    content_y0 = y_end
    content_y1 = y_start
    
    drawings = page.get_drawings()
    for d in drawings:
        r = d["rect"]
        if r.y1 > y_start and r.y0 < y_end:
            content_y0 = min(content_y0, max(y_start, r.y0))
            content_y1 = max(content_y1, min(y_end, r.y1))

    for b in blocks:
        by0, by1 = b[1], b[3]
        if by1 > y_start and by0 < y_end:
            if b[4].strip() == "":
                if b[6] != 1:
                    continue
            
            text_str = b[4].strip()
            if re.match(r"^\-\s*\d+\s*\-$", text_str):
                continue
                
            content_y0 = min(content_y0, max(y_start, by0))
            content_y1 = max(content_y1, min(y_end, by1))

    pad = 10
    final_y0 = max(y_start, content_y0 - pad)
    final_y1 = min(y_end, content_y1 + pad)
    
    if final_y1 <= final_y0:
        return None
        
    return fitz.Rect(0, final_y0, page.rect.x1, final_y1)


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
        
        for q in range(1, 81):
            if q in q_positions:
                continue
                
            rects = page.search_for(f"Q{q}.")
            if not rects:
                rects = page.search_for(f"Q{q} ")
                
            if rects:
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
    q_positions[81] = (doc.page_count - 1, doc[doc.page_count - 1].rect.y1)

    extracted_texts = {}

    for q in range(1, 81):
        if q not in q_positions or (q + 1) not in q_positions:
            continue
            
        start_p, start_y = q_positions[q]
        end_p, end_y = q_positions[q + 1]
        
        # 1. Extract Text
        text = ""
        for p in range(start_p, end_p + 1):
            page = doc[p]
            rect = page.rect
            y0 = start_y if p == start_p else 0
            y1 = end_y if p == end_p else rect.y1
            
            clip = fitz.Rect(0, y0, rect.x1, y1)
            text += page.get_text(clip=clip) + "\n"
            
        # 2. Crop Image
        part = 1
        image_tags = []
        for p in range(start_p, end_p + 1):
            page = doc[p]
            rect = page.rect
            y0 = start_y if p == start_p else 0
            y1 = end_y if p == end_p else rect.y1
            
            tight_clip = get_tight_clip(page, y0, y1)
            if not tight_clip or (tight_clip.y1 - tight_clip.y0 < 20):
                continue
                
            pix = page.get_pixmap(clip=tight_clip, dpi=150)
            
            suffix = "_full" if start_p == end_p else f"_p{part}"
            filename = f"{base_name}_Q{q}{suffix}.png"
            out_path = os.path.join(out_dir, filename)
            pix.save(out_path)
            image_tags.append(f"![[{filename}]]")
            part += 1

        extracted_texts[str(q)] = text + "\n\n" + "\n".join(image_tags)

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
