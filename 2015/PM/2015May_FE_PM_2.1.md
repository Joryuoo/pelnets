---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - information-management
  - year/2015
---
# 2015May_FE_PM_2.1

![[2015May_FE_PM_Q2_Body_p1.png]]
![[2015May_FE_PM_Q2_SQ1_p1.png]]

?

d, d, b

### Explanation

**Blank A:**
The scenario states, "Each subject has mark items such as exercises, tests, and final exam...". This indicates that a single subject can have multiple mark categories associated with it. Therefore, the missing one-to-many relationship must be from **Subject** to **MarksCategory**.
- **Correct Answer for A: d) Subject**

**Blank B:**
The `MarksCategory` table defines the different grading components (mark items) and their percentages for a specific subject. To uniquely identify a mark category, we need to know which subject it belongs to and the specific mark ID (e.g., Test, Final exam). Thus, the composite primary key for `MarksCategory` should be `SubjectID` and `MarksID`. Since `MarksID` is already listed in `MarksCategory`, Blank B must be **SubjectID**.
- **Correct Answer for B: d) SubjectID**

**Blank C:**
The `Marks` table records the actual scores achieved by students. To uniquely identify a specific score, the database needs to know the student (`StudentID`), the subject (`SubjectID`), and the specific mark category (`MarksID`). The `Marks` table already lists `StudentID` and `___B___` (which we determined is `SubjectID`). Therefore, Blank C must be the remaining necessary key to identify the specific mark item, **MarksID**.
- **Correct Answer for C: b) MarksID**

**Why other choices are incorrect:**
- **For A:** `Class`, `ClassSubject`, and `Student` do not dictate the mark items. The requirements explicitly state that the mark items belong to the *subject*.
- **For B and C:** `ClassID` is incorrect because the mark items are determined per subject, not per class. `StudentID` is already present in the `Marks` table and does not belong in `MarksCategory` because categories are defined independently of individual students.
