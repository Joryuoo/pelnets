---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - algorithms
  - data-structures
  - year/2015
---
# 2015May_FE_PM_6.1

![[2015May_FE_PM_Q6_Body_p1.png]]
![[2015May_FE_PM_Q6_Body_p2.png]]
![[2015May_FE_PM_Q6_SQ1_p1.png]]

?
A=a, B=b

### Explanation

The `Heapify` function needs to calculate the index of the left child (`lChild`) and right child (`rChild`) for a given node at index `i`.

According to the rules of a binary heap implemented as a 1-indexed array (which is explicitly stated in Program Description item 2):
* The index of the left child is $2 \times i$.
* The index of the right child is $2 \times i + 1$.
* The index of the parent is $i \div 2$.

Therefore:
* **Blank A (`lChild`):** Must be $2 \times i$, which corresponds to choice **a**.
* **Blank B (`rChild`):** Must be $2 \times i + 1$, which corresponds to choice **b**.

**Why other options are incorrect:**
* **c) $2 \times i + 2$:** This does not correspond to any valid relative node in a standard binary tree structure. 
* **d) $i \div 2$:** This calculates the index of the **parent** node, not the child nodes.
