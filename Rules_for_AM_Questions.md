# Rules for PhilNITS AM (Morning) Questions

When processing AM (Morning) exam questions (e.g., `2021A_FE_AM`, `2022S_FE_AM`), these strict rules MUST be followed to prevent hallucination, save tokens, and ensure flawless formatting. 

These rules supersede any previous conventions when dealing with AM questions.

## 1. File Naming and Header
* **File Name:** `{Year}{Season}_FE_AM_{QuestionNumber}.md` (e.g., `2021A_FE_AM_25.md`)
* **H1 Header:** Must exactly match the filename without the extension: `# {Year}{Season}_FE_AM_{QuestionNumber}`
* **No Question Prefix:** Do **NOT** start the actual question text with `Q1.` or `Q{number}.` The H1 header is sufficient.

## 2. YAML Metadata and Strict Tags
Every flashcard must have this exact YAML block:
```yaml
---
created: YYYY-MM-DD HH:mm
status: "#philnits"
tags:
  - software/YYYY
  - software/YYYY
  - year/YYYY
---
```
* **Strict Tag List:** You may ONLY select 1 to 3 categories from this exact list:
  `number-systems`, `operating-systems`, `project-management`, `accounting`, `probability`, `cybersecurity`, `systems-architecture`, `sets`, `digital-logic`, `algorithms`, `hardware`, `service-management`, `data-structures`, `programming`, `web-technologies`, `information-management`, `statistics`, `networking`, `math`, `business-administration`, `software`, `software-testing`, `software-engineering`, `devops`, `object-oriented-programming`, `automata-theory`, `data-encoding`, `cloud-computing`, `artificial-intelligence`
* **NO INVENTED TAGS:** Do not use `database`, `multimedia`, `security`, `PhilNITS`, etc. Map them to the allowed list (e.g., `information-management`, `data-encoding`, `cybersecurity`).
* **Year Tag:** The final tag must always be `year/YYYY`.

## 3. Pure Text vs. Image Questions
To avoid token bloat and OCR errors, questions are strictly categorized into two types:

### A. Pure Text Questions
If the question is entirely plain text (no tables, diagrams, code blocks, or complex math/inequalities):
* Type out the complete question text manually.
* Type out the choices `a)`, `b)`, `c)`, `d)`.
* Do **NOT** include an image link.

### B. Image / Complex Questions
If the question contains ANY tables, diagrams, code blocks, or complex math:
* **DO NOT** type out the question text.
* Embed a screenshot exactly like this: `![[{Year}{Season}_FE_AM_Q{QuestionNumber}_full.png]]`
* Do **NOT** ever output placeholders like `*(Visualization omitted to save tokens)*`.
* You may still type out the `a, b, c, d` choices below the image if the choices themselves are simple text, but never the complex question body.

## 4. The Separator and Answer
* The separator must be a single `?` on a new line.
* The line immediately following `?` must be the correct answer letter and the text (e.g., `c) NAPT`).

## 5. Explanations (Strictly NO Mermaid)
* Include a `### Explanation` section.
* **CRITICAL:** Do **NOT** use Mermaid charts or diagrams under any circumstances to save tokens.
* Use plain text, bullet points, markdown tables, or LaTeX to explain the concept step-by-step.
* The explanation must align with the official answer key. If the official question has a typo but the answer key expects a certain answer, explain the answer key's logic.

---

### Example Template (Pure Text)
```md
---
created: 2026-09-09 23:30
status: "#philnits"
tags:
  - networking/2021
  - year/2021
---
# 2021A_FE_AM_31
Which of the following is a mechanism that enables multiple terminals to have private addresses different from each other to connect to the Internet by sharing a single global IP address?

a) DHCP
b) DNS
c) NAPT
d) RADIUS
?
c) NAPT
### Explanation
NAPT (Network Address Port Translation) translates private IP addresses and port numbers...
```

### Example Template (Image-based)
```md
---
created: 2026-09-09 23:30
status: "#philnits"
tags:
  - software-engineering/2021
  - information-management/2021
  - year/2021
---
# 2021A_FE_AM_25
![[2021A_FE_AM_Q25_full.png]]

a) A (1..1), B (1..1), C (1..*), D (1..*)
b) A (1..1), B (1..*), C (1..1), D (1..*)
c) A (1..*), B (1..1), C (1..*), D (1..1)
d) A (1..*), B (1..*), C (1..1), D (1..*)
?
b) A (1..1), B (1..*), C (1..1), D (1..*)
### Explanation
The problem states that "each continent has at least one country"...
```

## 6. Targeted Context (Token Optimization)
To prevent API quota limits and token bloat during generation, AI subagents should not be forced to read massive JSON files containing the entire exam. Instead, the orchestrating script must extract the specific raw text for the assigned question(s) and save it to a small, isolated temporary file (e.g., scratch/Q1_context.txt). The subagent is then instructed to read ONLY this isolated text file to get its context.

## 7. Model Restrictions
- **NEVER USE ANY FLASH MODEL.** Under absolutely no circumstances should `flash` OR `flash_lite` be used. All generation, whether in the main thread or via subagents, MUST use the primary model (e.g., by selecting `inherit` for subagents). All Flash-family models are strictly banned.
