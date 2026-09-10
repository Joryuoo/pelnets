import fitz
import sys
import re

def extract_answers(pdf_path, output_txt_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
        
    # The AM answers are typically simple tables mapping Q number to a letter
    # For example: 
    # Q No. Ans.
    # 1 a
    # 2 c
    
    # Let's find patterns like "1 a", "1\n \na", etc.
    # Usually it's better to just regex capture all standalone letters that might be answers, but let's try a robust approach.
    
    answers = {}
    
    # Split text by lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Simple heuristic: Look for lines that are just numbers 1-80, followed soon after by a,b,c,d,e
    current_q = None
    for line in lines:
        if line.isdigit():
            num = int(line)
            if 1 <= num <= 80:
                current_q = num
        elif current_q and len(line) == 1 and line.lower() in ['a', 'b', 'c', 'd', 'e']:
            answers[current_q] = line.lower()
            current_q = None
            
    if not answers or len(answers) < 80:
        # fallback: try regex
        text_clean = text.replace('\n', ' ')
        # Matches: "1 a", "2 b", etc. Sometimes they are separated by spaces or tabs
        matches = re.findall(r'\b([1-8][0-9]?)\s+([a-e])\b', text_clean, re.IGNORECASE)
        for m in matches:
            q = int(m[0])
            ans = m[1].lower()
            if 1 <= q <= 80 and q not in answers:
                answers[q] = ans

    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for q in range(1, 81):
            if q in answers:
                f.write(f"Q{q}: {answers[q]}\n")
            else:
                f.write(f"Q{q}: MISSING\n")
                
    print(f"Extracted {len(answers)} answers to {output_txt_path}")

if __name__ == "__main__":
    extract_answers(sys.argv[1], sys.argv[2])
