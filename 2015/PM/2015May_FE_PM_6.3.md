---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - algorithms
  - data-structures
  - year/2015
---
# 2015May_FE_PM_6.3

![[2015May_FE_PM_Q6_SQ3_p1.png]]

?
c

### Explanation
The question asks for the values in the array `A[]` after `BuildHeap(A, n)` completes for an initial array of `n = 7`.

The initial array `A[]` is:
`[2, 5, 6, 3, 7, 8, 4]`

The `BuildHeap` function builds a max heap by calling `Heapify` starting from `i = n ÷ 2` down to `1`.
For `n = 7`, `i` will iterate backwards through `3`, `2`, and `1`.

**Step 1: i = 3**
* `Heapify(A, 3, 7)` is called.
* The parent node is `A[3] = 6`.
* Left child `A[6] = 8`, Right child `A[7] = 4`.
* The largest among the three is the left child (`8`).
* Swap `A[3]` and `A[6]`.
* Array becomes: `[2, 5, 8, 3, 7, 6, 4]`.
* `Heapify` is recursively called on index `6`, but since it has no children within `heapsize = 7`, it returns.

**Step 2: i = 2**
* `Heapify(A, 2, 7)` is called.
* The parent node is `A[2] = 5`.
* Left child `A[4] = 3`, Right child `A[5] = 7`.
* The largest among the three is the right child (`7`).
* Swap `A[2]` and `A[5]`.
* Array becomes: `[2, 7, 8, 3, 5, 6, 4]`.
* `Heapify` is recursively called on index `5`, but it has no children, so it returns.

**Step 3: i = 1**
* `Heapify(A, 1, 7)` is called.
* The parent node is `A[1] = 2`.
* Left child `A[2] = 7`, Right child `A[3] = 8`.
* The largest among the three is the right child (`8`).
* Swap `A[1]` and `A[3]`.
* Array becomes: `[8, 7, 2, 3, 5, 6, 4]`.
* `Heapify(A, 3, 7)` is recursively called because `A[3]` was modified.

**Step 4: Recursive Heapify for i = 3**
* The parent node is now `A[3] = 2`.
* Left child `A[6] = 6`, Right child `A[7] = 4`.
* The largest among the three is the left child (`6`).
* Swap `A[3]` and `A[6]`.
* Array becomes: `[8, 7, 6, 3, 5, 2, 4]`.
* `Heapify(A, 6, 7)` is called, but `A[6]` has no children, so it returns.

**Final Result:**
The array `A[]` is `[8, 7, 6, 3, 5, 2, 4]`.
This matches choice **c**.
