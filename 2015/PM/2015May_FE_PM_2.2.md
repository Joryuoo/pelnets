---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - information-management/2015
  - year/2015
---
# 2015May_FE_PM_2.2

![[2015May_FE_PM_Q2_SQ2_p1.png]]
![[2015May_FE_PM_Q2_SQ2_p2.png]]

?
D=g, E=c, F=d

### Explanation
This subquestion asks us to complete an SQL statement that calculates the total marks for each student for a given class and subject.

* **Blank D:** The column `TotalMarks` needs to be calculated. The problem states: "Total marks of each student is sum of individual marks of mark items multiplied with their contribution percentages... ÷ 100". The SQL expression for this is `SUM(Marks * Percentage) / 100`. Thus, **g** is the correct answer. Choice **a** `AVG(...)` is incorrect because we need the sum of the weighted marks, not the average.

* **Blank E:** This blank represents the `WHERE` clause joining conditions. The query selects from `Class, Student, Marks, MarksCategory`. 
The joins already specified are:
`Class.ClassID = :ClassID`
`Marks.SubjectID = :SubjectID`
`Class.ClassID = Student.ClassID`

We need to join `Student` with `Marks`, and `Marks` with `MarksCategory`.
`Student` and `Marks` are joined on `StudentID`: `Student.StudentID = Marks.StudentID`.
`Marks` and `MarksCategory` must be joined on both `SubjectID` and `MarksID` because `MarksCategory` uses both to identify a specific mark item.
Therefore, `Student.StudentID = Marks.StudentID AND Marks.SubjectID = MarksCategory.SubjectID AND Marks.MarksID = MarksCategory.MarksID`. This matches choice **c**. 
Choice **b** is incorrect because it misses the `Marks.MarksID = MarksCategory.MarksID` condition, which would result in a Cartesian product when querying marks for a subject.

* **Blank F:** This blank represents the `GROUP BY` clause. The `SELECT` list includes `Student.StudentID, StudentName` and an aggregate function `SUM(...)`. In SQL, all non-aggregated columns in the `SELECT` clause must appear in the `GROUP BY` clause. Therefore, we must group by `Student.StudentID, StudentName`. This matches choice **d**. 
Choice **e** (`StudentID`) is incorrect as it omits `StudentName`, which would cause a SQL syntax error. Choice **f** (`StudentID, StudentName`) lacks the table alias for `StudentID`, which is ambiguous since `StudentID` exists in both `Student` and `Marks` tables.
