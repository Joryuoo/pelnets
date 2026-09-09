import json
import os

with open(r"C:\Users\Kyle\Downloads\pelnets\2021A_questions_text.json", "r", encoding="utf-8") as f:
    questions = json.load(f)
    
with open(r"C:\Users\Kyle\Downloads\pelnets\2021A_answers.json", "r", encoding="utf-8") as f:
    answers = json.load(f)
    
data = {}
for i in range(1, 81):
    data[str(i)] = {
        "text": questions[str(i)],
        "answer": answers[str(i)]
    }

# Split into 8 batches of 10
for b in range(8):
    batch_data = {str(k): data[str(k)] for k in range(b*10 + 1, b*10 + 11)}
    with open(f"C:\\Users\\Kyle\\Downloads\\pelnets\\batch_{b+1}.json", "w", encoding="utf-8") as f:
        json.dump(batch_data, f, indent=2, ensure_ascii=False)

print("Created 8 batches.")
