import json

subagents = []

answers = {
    "1.1": "c",
    "1.2": "f",
    "1.3": "b, d",
    "1.4": "f, d",
    "2.1": "e",
    "2.2": "d",
    "2.3": "c",
    "2.4": "a",
    "2.5": "c",
    "3.1": "d",
    "3.2": "a",
    "4.1": "d, d, f, c",
    "4.2": "d, e",
    "5.1": "c, c, a",
    "5.2": "b",
    "6.1": "d, g, d, a",
    "7.1": "b, a, c",
    "8.1": "a, b, a, f",
    "8.2": "d",
    "9.1": "d, c, b, c, c"
}

# Group subquestions by question number
questions = {}
for sq, ans in answers.items():
    q = sq.split(".")[0]
    questions.setdefault(q, []).append((sq, ans))

for q, sq_list in questions.items():
    sq_keys_str = ", ".join([f'"{sq}"' for sq, _ in sq_list])
    expected_output_str = "\n".join([f"Subquestion {sq} EXPECTED STRICT OUTPUT: {ans}" for sq, ans in sq_list])
    
    prompt = f"""You are an expert IT instructor. Generate the JSON data for PhilNITS PM Question {q} (which includes subquestions {sq_keys_str}) of the 2007A_FE_PM exam.
Your output must be written to `C:\\Users\\Kyle\\Downloads\\pelnets\\.exam_work\\2007A_PM\\review_q{q}.json` using `write_to_file`.

For each subquestion key `k` in {sq_keys_str}:
1. Read the raw text for this subquestion from `C:\\Users\\Kyle\\Downloads\\pelnets\\.exam_work\\2007A_PM\\contexts\\{{k}}.txt` using `view_file`. NOTE: The text for the overall scenario is usually included in the `.1` context.
2. Form the JSON object for this subquestion key:
   - `topics`: An array of 1 to 3 string tags from the strict allowed list in `Rules_for_PM_Questions.md` (e.g. `["cybersecurity", "networking"]`). Do not include the year suffix.
   - `answer`: STRICTLY the comma-separated lowercase letters of the answers for this subquestion exactly as provided in the expected strict output below. No spaces before the first letter, just "a, b, c".
   - `explanation`: A detailed markdown explanation explaining the correct logic. Briefly explain why incorrect choices are wrong if educational. DO NOT USE MERMAID CHARTS. You may use manual text tables if helpful.

Here are the answer keys for this question:
{expected_output_str}

Your final output file must be a single valid JSON object whose keys are the string subquestion numbers (e.g., "{sq_list[0][0]}").
Do not wrap it in markdown code blocks inside the file. Note that your `write_to_file` will just contain the raw JSON."""

    subagents.append({
        "Model": "pro",
        "TypeName": "self",
        "Role": f"2007A PM Q{q}",
        "Prompt": prompt
    })

with open("launch_2007a_pm.json", "w", encoding="utf-8") as f:
    json.dump({"Subagents": subagents}, f, indent=2)

print(f"Generated launch json for {len(subagents)} PM subagents.")
