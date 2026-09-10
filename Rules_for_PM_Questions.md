# Rules for Processing PM (Afternoon) Questions

PM (Afternoon) or Subject B exams have a very different format compared to AM exams. They consist of fewer questions (usually 8 to 11), but each question is a massive, multi-page scenario with several subquestions and blanks to fill in.

To ensure consistency, readability, and token efficiency, strictly follow these rules when processing PM exams:

## 1. File Splitting (One File Per Subquestion)
- **DO NOT** dump an entire PM question into a single flashcard file.
- Split the PM question into separate markdown files based on its **Subquestions**.
- **Naming Convention:** `[Year][Season]_FE_PM_[Q].[SQ].md`
  - *Example:* For Question 1, if it has 2 subquestions, create `2021S_FE_PM_1.1.md` and `2021S_FE_PM_1.2.md`.
- Store all PM files in their respective `[Year]/PM/` folder.

## 2. Image Cropping and Embedding (Context Rules)
- **DO NOT** type out the massive question scenario text. Use screenshots.
- PM questions must be precisely cropped into chunks based on the Y-coordinates of the "Subquestion X" headers using a PDF library (like `pymupdf`/`fitz`).
- **Subquestion 1 (`.1.md`) Context:** Embed screenshots of the **entire scenario body** plus the text/choices for Subquestion 1. This provides the user with the foundational context when they first encounter the problem.
  - *Example Embeds:* `![[2021S_FE_PM_Q1_Body_p1.png]]`, `![[2021S_FE_PM_Q1_SQ1_p1.png]]`
- **Subquestion 2+ (`.2.md`, `.3.md`) Context:** **ONLY** embed the specifically cropped image of that subquestion and its choices. Do not re-embed the entire scenario body to avoid redundant scrolling.
  - *Example Embeds:* `![[2021S_FE_PM_Q1_SQ2_p1.png]]`

## 3. Answer Formatting
- Use a single `?` on its own line to separate the question (images) from the back of the flashcard.
- Directly underneath the `?`, provide the answers as a **simple comma-separated list of letters** corresponding to the blanks for that specific subquestion.
  - *Example:* If Subquestion 1 has blanks A, B, C, and D, the answer line should just be: `c, d, b, c`
  - Do not re-type the text of the choices.

## 4. Explanation Generation
- Start the explanation section with `### Explanation`.
- The AI/Subagent generating the explanation **must** be provided with the raw extracted text of the PM question (e.g., via a temporary JSON file). It cannot accurately explain complex algorithms, routing tables, or Java code tracing without reading the scenario.
- **NO MERMAID CHARTS:** To save tokens, do not use Mermaid diagrams. Use standard markdown text, bullet points, and markdown tables to trace execution steps or variable states.

## 5. YAML Metadata and Tagging
- **Strict Tag List:** You may select multiple categories if the question heavily features them, but you MUST ONLY select from this exact list:
  `number-systems`, `operating-systems`, `project-management`, `accounting`, `probability`, `cybersecurity`, `systems-architecture`, `sets`, `digital-logic`, `algorithms`, `hardware`, `service-management`, `data-structures`, `programming`, `web-technologies`, `information-management`, `statistics`, `networking`, `math`, `business-administration`, `software`, `software-testing`, `software-engineering`, `devops`, `object-oriented-programming`, `automata-theory`, `data-encoding`, `cloud-computing`, `artificial-intelligence`
- **NO INVENTED TAGS:** Do not use `database`, `multimedia`, `security`, `PhilNITS`, etc. Map them to the allowed list (e.g., `information-management`, `data-encoding`, `cybersecurity`).
- Format:
```yaml
---
created: YYYY-MM-DD HH:MM
status: "#philnits"
tags:
  - software/<year>
  - year/<year>
---
```

## 6. Model and Execution Rules
- **Do not use subagents:** Process questions sequentially and manually in the main thread. Do not orchestrate or invoke subagents for question processing.
- **Stick to the current model:** Do not use `flash` or any other model. Use the primary model for all processing.
- **Targeted Context (Token Optimization):** To prevent API quota limits and token bloat during generation, you should not be forced to read massive JSON files containing the entire exam all at once. Instead, extract the specific raw text for the assigned question(s) and save it to a small, isolated temporary file (e.g., scratch/Q1_context.txt). Then read ONLY this isolated text file to get context for generation.
