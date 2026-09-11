---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - algorithms
  - data-structures
  - year/2015
---
# 2015May_FE_PM_6.2

![[2015May_FE_PM_Q6_SQ2_p1.png]]
![[2015May_FE_PM_Q6_SQ2_p2.png]]

?
b, c, f, e

### Explanation

**Blanks C and D:**
`BuildHeap` calls `Heapify(A, i, n)` starting from `i = n ÷ 2`. For `n = 5`, the loop runs for `i = 2` and then `i = 1`. 
The initial array is `A = [3, 5, 7, 1, 9]`.

**1st Call:** `Heapify(A, 2, 5)`
- `i = 2`. `lChild = 4`, `rChild = 5`.
- Compare `A[lChild]` (1) with `A[i]` (5). 1 is not greater than 5, so `largest = i = 2`. (Line X is not executed)
- Compare `A[rChild]` (9) with `A[largest]` (5). 9 is greater than 5, so `largest = rChild = 5`. (Line Y is executed)
- Swap `A[2]` and `A[5]`. Array becomes `[3, 9, 7, 1, 5]`.
- Recursive call `Heapify(A, 5, 5)` does nothing since children indices > 5.

**2nd Call:** `Heapify(A, 1, 5)`
- `i = 1`. `lChild = 2`, `rChild = 3`.
- Compare `A[lChild]` (9) with `A[i]` (3). 9 is greater than 3, so `largest = lChild = 2`. (Line X is executed)
- Compare `A[rChild]` (7) with `A[largest]` (9). 7 is not greater than 9.
- Swap `A[1]` and `A[2]`. Array becomes `[9, 3, 7, 1, 5]`.
- Recursive call `Heapify(A, 2, 5)`.
  - `i = 2`. `lChild = 4`, `rChild = 5`.
  - Compare `A[4]` (1) with `A[2]` (3). Not greater. `largest = 2`. (Line X is not executed)
  - Compare `A[5]` (5) with `A[2]` (3). Greater! `largest = rChild = 5`. (Line Y is executed)
  - Swap `A[2]` and `A[5]`. Array becomes `[9, 5, 7, 1, 3]`.

Counting executions: Line X was executed 1 time (**C = b**). Line Y was executed 2 times (**D = c**).

**Blanks E and F:**
Blank E represents the heap after the 1st iteration of the sorting loop.
Before iteration 1: `A = [9, 5, 7, 1, 3]`
- **Step 1:** Swap `A[1]` (9) with `A[5]` (3). `A = [3, 5, 7, 1, 9]`. (9 is now sorted).
- **Step 2:** Heap size `i` becomes 4.
- **Step 3:** Call `Heapify(A, 1, 4)` on `[3, 5, 7, 1]`.
  - `i = 1`, children are indices 2 and 3 (`A[2]=5`, `A[3]=7`).
  - Max child is `A[3]=7`. Swap `A[1]` and `A[3]`.
  - Array becomes `[7, 5, 3, 1]`.
  - Recursive call to index 3 has no valid children within heap size 4.
- Resulting heap for E is `[7, 5, 3, 1]`, which corresponds to **E = f**.

Blank F represents the heap after the 2nd iteration of the sorting loop.
Before iteration 2: `A = [7, 5, 3, 1, 9]`
- **Step 1:** Swap `A[1]` (7) with `A[4]` (1). `A = [1, 5, 3, 7, 9]`. (7 and 9 are now sorted).
- **Step 2:** Heap size `i` becomes 3.
- **Step 3:** Call `Heapify(A, 1, 3)` on `[1, 5, 3]`.
  - `i = 1`, children are indices 2 and 3 (`A[2]=5`, `A[3]=3`).
  - Max child is `A[2]=5`. Swap `A[1]` and `A[2]`.
  - Array becomes `[5, 1, 3]`.
  - Recursive call to index 2 has no valid children within heap size 3.
- Resulting heap for F is `[5, 1, 3]`, which corresponds to **F = e**.
