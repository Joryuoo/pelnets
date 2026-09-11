---
created: 2026-09-11 09:39
status: "#philnits"
tags:
  - operating-systems
  - year/2015
---

# 2015May_FE_PM_1.1

![[2015May_FE_PM_Q1_Body_p1.png]]
![[2015May_FE_PM_Q1_SQ1_p1.png]]
![[2015May_FE_PM_Q1_SQ1_p2.png]]

?
A=f, B=e, C=e

### Explanation

We are tracking a data buffer with a capacity of 5 slots using the **First-In-First-Out (FIFO)** replacement algorithm. In FIFO, when a new block must be loaded and the buffer is full, the block that has been in the buffer the longest is replaced. Accessing/hitting a block that is already in the buffer does *not* reset its age.

Initially, the buffer is loaded with `[1] [2] [3] [4] [5]`. Thus, the FIFO queue tracking the oldest to newest elements is `1, 2, 3, 4, 5`.

Let's trace the access sequence: 
`[1] [2] [3] [5] [6] [1] [2] [3] [4] [6] [1] [2] [5] [6] [4] [1] [2]`

- **Access `[1], [2], [3], [5]`**: All four accesses are Hits (data is already in the buffer). The buffer remains `[1, 2, 3, 4, 5]`. Replacements: 0.
- **Access `[6]`**: Miss. Replaces the oldest block `[1]`. Buffer becomes `[6, 2, 3, 4, 5]`. FIFO queue: `2, 3, 4, 5, 6`. Replacements: 1.
- **Access `[1]`**: Miss. Replaces oldest `[2]`. Buffer becomes `[6, 1, 3, 4, 5]`. FIFO queue: `3, 4, 5, 6, 1`. Replacements: 2.
- **Access `[2]`**: Miss. Replaces oldest `[3]`. Buffer becomes `[6, 1, 2, 4, 5]`. FIFO queue: `4, 5, 6, 1, 2`. Replacements: 3.
- **Access `[3]`**: Miss. Replaces oldest `[4]`. Buffer becomes `[6, 1, 2, 3, 5]`. FIFO queue: `5, 6, 1, 2, 3`. Replacements: 4.
- **Access `[4]`**: Miss. Replaces oldest `[5]`. Buffer becomes `[6, 1, 2, 3, 4]`. FIFO queue: `6, 1, 2, 3, 4`. Replacements: 5.
- **Access `[6]`**: Hit. Buffer remains `[6, 1, 2, 3, 4]`. Replacements: 5.
  - *This is the point ▼ shown in the diagram immediately after the second `[6]` is accessed. The buffer state is `[6] [1] [2] [3] [4]`. Therefore, Blank A corresponds to choice **f**.*

Continuing the sequence from point ▼:
- **Access `[1], [2]`**: Both are Hits. Buffer remains `[6, 1, 2, 3, 4]`.
- **Access `[5]`**: Miss. Replaces oldest `[6]`. Buffer becomes `[5, 1, 2, 3, 4]`. FIFO queue: `1, 2, 3, 4, 5`. Replacements: 6.
- **Access `[6]`**: Miss. Replaces oldest `[1]`. Buffer becomes `[5, 6, 2, 3, 4]`. FIFO queue: `2, 3, 4, 5, 6`. Replacements: 7.
- **Access `[4]`**: Hit. Buffer remains `[5, 6, 2, 3, 4]`.
- **Access `[1]`**: Miss. Replaces oldest `[2]`. Buffer becomes `[5, 6, 1, 3, 4]`. FIFO queue: `3, 4, 5, 6, 1`. Replacements: 8.
- **Access `[2]`**: Miss. Replaces oldest `[3]`. Buffer becomes `[5, 6, 1, 2, 4]`. FIFO queue: `4, 5, 6, 1, 2`. Replacements: 9.
  - *This is the end of the entire access series. The final buffer state is `[5] [6] [1] [2] [4]`. Therefore, Blank B corresponds to choice **e**.*
  - *The total number of block replacements across the entire duration is **9**. Therefore, Blank C corresponds to choice **e**.*

*(Note: Incorrect choices generally represent applying LRU/MFU logic mistakenly, where recent accesses might alter block priorities, or miscounting the linear queue rotations.)*
