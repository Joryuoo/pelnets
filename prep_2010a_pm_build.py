import json

subagents = []

prompts = [
    {
        "q": "1",
        "keys": ["1.1"],
        "answers": {
            "1.1": "c, b, c, b, a"
        }
    },
    {
        "q": "2",
        "keys": ["2.1", "2.2"],
        "answers": {
            "2.1": "h, a, b",
            "2.2": "d, b, c, e"
        }
    },
    {
        "q": "3",
        "keys": ["3.1"],
        "answers": {
            "3.1": "c, b, c, c"
        }
    },
    {
        "q": "4",
        "keys": ["4.1"],
        "answers": {
            "4.1": "f, g, d, b, e, c"
        }
    },
    {
        "q": "5",
        "keys": ["5.1", "5.2"],
        "answers": {
            "5.1": "b, a, b, d, c",
            "5.2": "b"
        }
    },
    {
        "q": "6",
        "keys": ["6.1", "6.2"],
        "answers": {
            "6.1": "b, e, a, d",
            "6.2": "b, c"
        }
    },
    {
        "q": "7",
        "keys": ["7.1"],
        "answers": {
            "7.1": "e, d, g, b, a"
        }
    },
    {
        "q": "8",
        "keys": ["8.1"],
        "answers": {
            "8.1": "b, a, g, c, a, e, g"
        }
    }
]

for p in prompts:
    q = p["q"]
    keys_str = ", ".join([f'"{k}"' for k in p["keys"]])
    ans_map_str = "\n".join([f"Subquestion {k} EXPECTED STRICT OUTPUT: {ans}" for k, ans in p["answers"].items()])
    
    prompt = f"""You are an expert IT instructor. Generate the JSON data for PhilNITS PM Question {q} (which includes subquestions {keys_str}) of the 2010A_FE_PM exam.
Your output must be written to `C:\\Users\\Kyle\\Downloads\\pelnets\\.exam_work\\2010A_PM\\review_q{q}.json` using `write_to_file`.

For each subquestion key `k` in {keys_str}:
1. Read the raw text for this subquestion from `C:\\Users\\Kyle\\Downloads\\pelnets\\.exam_work\\2010A_PM\\contexts\\{{k}}.txt` using `view_file`. NOTE: The text for the overall scenario is usually included in the `.1` context.
2. Form the JSON object for this subquestion key:
   - `topics`: An array of 1 to 3 string tags from the strict allowed list in `Rules_for_PM_Questions.md` (e.g. `["cybersecurity", "networking"]`). Do not include the year suffix.
   - `answer`: STRICTLY the comma-separated lowercase letters of the answers for this subquestion exactly as provided in the expected strict output below. No spaces before the first letter, just "a, b, c".
   - `explanation`: A detailed markdown explanation explaining the correct logic. Briefly explain why incorrect choices are wrong if educational. DO NOT USE MERMAID CHARTS. You may use manual text tables if helpful.

Here are the answer keys for this question:
{ans_map_str}

Your final output file must be a single valid JSON object whose keys are the string subquestion numbers (e.g., "1.1").
Do not wrap it in markdown code blocks inside the file. Note that your `write_to_file` will just contain the raw JSON."""

    subagents.append({
        "Model": "pro",
        "TypeName": "self",
        "Role": f"2010A PM Q{q}",
        "Prompt": prompt
    })

with open("launch_2010a_pm.json", "w", encoding="utf-8") as f:
    json.dump({"Subagents": subagents}, f, indent=2)

print(f"Generated launch json for {len(subagents)} PM subagents.")
