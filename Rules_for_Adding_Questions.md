# Rules for Adding New PhilNITS Questions

When automatically or manually generating new flashcard notes for the PhilNITS exams based on the PDF question and answer keys, the following strict rules and conventions must be followed.

## 1. File Naming and Location
* **Naming Convention:** `{Year}{Season}_FE-{Paper}_{QuestionNumber}.md` 
  * *Example:* `2025A_FE-A_21.md` or `2025S_FE-A_1.md`
* **Location:** Save the file in the designated year folder (e.g., `2025/`). Do NOT overwrite any existing draft notes (like `2025S_FE_AM_1.md`) unless explicitly instructed.

## 2. Metadata (Frontmatter)
Every flashcard must begin with the following metadata tags so the Spaced Repetition plugin and vault organization work correctly:
```md
Created: YYYY-MM-DD HH:mm
Category: #appropriate-category
Status: #philnits
```
*Note: Refer to the `README.md` for the list of available categories (e.g., `#number-systems`, `#database`, etc.).*

## 3. Question Formatting (Front of Card)
The structure of the question side depends on the content of the question:

* **Standard Text Questions:** 
  Write out the full question text and all multiple-choice options (`a)` through `d)`).
* **Questions with Diagrams, Tables, Code, or Complex Formatting:** 
  If the question contains a diagram, flowchart, table, SQL code block, or heavily formatted lists (like `[Conditions]`), **do NOT type out the question text and choices**. 
  Instead, extract a screenshot of the *entire question block* from the PDF and save it in the `Files/` directory. 
  Embed the image directly under the H1 header like this:
  `![[{Year}{Season}_FE-{Paper}_Q{QuestionNumber}_full.png]]`

## 4. The Separator
Use a single `?` on a new line to separate the front of the flashcard (the question) from the back of the flashcard (the answer and explanation).

## 5. Answer and Explanation (Back of Card)
* **The Correct Answer:** The very first line after the `?` separator MUST be the correct answer exactly as it appears in the choices (e.g., `c) 14.0`).
* **Detailed Explanation:** 
  * Provide a section titled `### Explanation`.
  * The explanation must be **super detailed and step-by-step**. 
  * Use **Markdown tables** to trace state machines, memory states, or data structures.
  * Use **LaTeX formatting** (e.g., `$x^2 + y^2$`) for all mathematical formulas, calculations, and probability equations.

## 6. References
End the flashcard with a horizontal rule `---` followed by a `# References` section linking to the relevant topics discussed in the explanation.

---

### Example Template (Image-Based Question)
```md
Created: 2026-09-04 18:45
Category: #database #sql
Status: #philnits

# 2025A_FE-A_21

![[2025A_FE-A_Q21_full.png]]
?
a) department_id IN (SELECT department_id FROM Departments WHERE location = 'New York');

### Explanation
The subquery `(SELECT department_id FROM Departments WHERE location = 'New York')` retrieves...

---
# References
- [SQL Subqueries]
```
