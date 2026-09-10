import sys
import os
import json
import re
import fitz  # PyMuPDF

def get_tight_clip(page, y_start, y_end):
    blocks = page.get_text("blocks")
    content_y0 = y_end
    content_y1 = y_start
    
    # Also find drawing paths (lines, rectangles, etc.) that might not be text
    drawings = page.get_drawings()
    for d in drawings:
        r = d["rect"]
        if r.y1 > y_start and r.y0 < y_end:
            content_y0 = min(content_y0, max(y_start, r.y0))
            content_y1 = max(content_y1, min(y_end, r.y1))

    for b in blocks:
        # block tuple: (x0, y0, x1, y1, "text", block_no, block_type)
        by0, by1 = b[1], b[3]
        if by1 > y_start and by0 < y_end:
            # The block intersects our horizontal slice
            if b[4].strip() == "": # Skip empty text blocks
                # Still check if it's an image block (type 1)
                if b[6] != 1:
                    continue
            
            # Skip page numbers like "- 12 -"
            text_str = b[4].strip()
            if re.match(r"^\-\s*\d+\s*\-$", text_str):
                continue
                
            content_y0 = min(content_y0, max(y_start, by0))
            content_y1 = max(content_y1, min(y_end, by1))

    # Add a small padding
    pad = 10
    final_y0 = max(y_start, content_y0 - pad)
    final_y1 = min(y_end, content_y1 + pad)
    
    # If we didn't find any content (empty page area), return None
    if final_y1 <= final_y0:
        return None
        
    return fitz.Rect(0, final_y0, page.rect.x1, final_y1)


def process_pm_pdf(pdf_path, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    doc = fitz.open(pdf_path)
    base_name = os.path.basename(pdf_path).replace("_Question.pdf", "")
    print(f"Processing {base_name}...")

    # 1. Find the starting page of each question Q1 to Q8
    q_starts = {}
    for p in range(doc.page_count):
        text = doc[p].get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines:
            match = re.match(r"^Q([1-8])\.\s*Read the following", line)
            if match:
                q_num = int(match.group(1))
                if q_num not in q_starts:
                    q_starts[q_num] = p
                    print(f"Detected Q{q_num} starting on page index {p}")

    if not q_starts:
        print("Could not detect any questions automatically. Exiting.")
        return

    # Sort questions to determine end pages
    sorted_qs = sorted(q_starts.keys())
    q_ends = {}
    for i in range(len(sorted_qs)):
        q = sorted_qs[i]
        if i < len(sorted_qs) - 1:
            q_ends[q] = q_starts[sorted_qs[i+1]] - 1
        else:
            q_ends[q] = doc.page_count - 1

    extracted_texts = {}

    # 2. Process each question
    for q in sorted_qs:
        start_p = q_starts[q]
        end_p = q_ends[q]

        # Extract Text
        text = ""
        for p in range(start_p, end_p + 1):
            text += doc[p].get_text() + "\n"
        extracted_texts[str(q)] = text

        # Find subquestions
        sq_positions = {}
        for sq in range(1, 10):
            found = False
            for p in range(start_p, end_p + 1):
                page = doc[p]
                
                # Try specific subquestion number
                rects = page.search_for(f"Subquestion {sq}")
                
                # Edge case: just "Subquestion" (happens when there's only 1 subquestion)
                if not rects and sq == 1:
                    rects = page.search_for("Subquestion")
                    # Filter out ones that are actually "Subquestions 1 and 2" in the header
                    rects = [r for r in rects if r.y0 > 100]

                if rects:
                    r = rects[0]
                    y0 = max(0, r.y0 - 20)
                    sq_positions[sq] = (p, y0)
                    found = True
                    break
            if not found:
                break
        
        num_sqs = len(sq_positions)
        print(f"  -> Q{q} spans pages {start_p} to {end_p}, found {num_sqs} subquestions.")

        boundaries = [(start_p, 0)]
        for i in range(1, num_sqs + 1):
            boundaries.append(sq_positions[i])
        boundaries.append((end_p, doc[end_p].rect.y1))

        # 3. Crop Images
        image_tags = []
        for chunk_idx in range(num_sqs + 1):
            c_start_p, c_start_y = boundaries[chunk_idx]
            c_end_p, c_end_y = boundaries[chunk_idx + 1]

            prefix = f"{base_name}_Q{q}_Body" if chunk_idx == 0 else f"{base_name}_Q{q}_SQ{chunk_idx}"
            part = 1
            for p in range(c_start_p, c_end_p + 1):
                page = doc[p]
                rect = page.rect
                y0 = c_start_y if p == c_start_p else 0
                y1 = c_end_y if p == c_end_p else rect.y1

                # Find a tight crop that removes massive white spaces at the top/bottom
                tight_clip = get_tight_clip(page, y0, y1)
                
                # Skip if crop area is too small or completely empty
                if not tight_clip or (tight_clip.y1 - tight_clip.y0 < 20):
                    continue

                pix = page.get_pixmap(clip=tight_clip, dpi=150)
                filename = f"{prefix}_p{part}.png"
                out_path = os.path.join(out_dir, filename)
                pix.save(out_path)
                image_tags.append(f"![[{filename}]]")
                part += 1

        extracted_texts[str(q)] = text + "\n\n" + "\n".join(image_tags)
    json_path = os.path.join(os.path.dirname(pdf_path), f"{base_name}_Questions_Text.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(extracted_texts, f, ensure_ascii=False, indent=2)
    print(f"Extraction complete! Saved JSON to {json_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python global_pm_processor.py <path_to_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    out_dir = r"C:\Users\Kyle\Downloads\pelnets\Files"
    process_pm_pdf(pdf_path, out_dir)
