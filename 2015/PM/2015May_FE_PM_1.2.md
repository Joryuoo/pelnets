---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - operating-systems
  - year/2015
---
# 2015May_FE_PM_1.2

![[2015May_FE_PM_Q1_SQ2_p1.png]]
![[2015May_FE_PM_Q1_SQ2_p2.png]]

?
D=d, E=a, F=b

### Explanation

**Blank D: d**
The program accesses 8 data blocks with a cyclic pattern: the first 3 data blocks are always accessed, followed by 2 of the remaining 5 data blocks. Since the data buffer holds 5 blocks, the 3 blocks that are consistently accessed every cycle will remain in the buffer permanently under both the MFU (they have the highest frequency of access) and LRU (they are frequently the most recently used) methods. The remaining 5 data blocks will compete for the remaining 2 buffer slots and thus be subject to replacement. This matches description **d**.
- *Why not c?* Statement c claims all 8 will be subject to replacement, which is false since the first 3 are always needed and will secure their place.

**Blank E: a**
Using the **Most Frequently Used (MFU)** method:
- The first 5 data blocks are accessed repeatedly (10 times each), giving them a high access count (10).
- When the program moves to the next 3 data blocks, the first new block accessed has an access count of 1. 
- Because MFU replaces the block with the *lowest* count, this new block (count 1) will be chosen as the victim for replacement when the *next* new block needs to be loaded. The original 5 blocks (count 10) are protected.
- Consequently, the first 5 blocks stay permanently, and the next 3 blocks will constantly replace each other. This matches description **a**.

**Blank F: b**
Using the **Least Recently Used (LRU)** method:
- The first 5 data blocks fit perfectly into the 5-block buffer, so no replacements happen during their repeated use.
- When the program starts accessing the next 3 data blocks, they will sequentially replace the least recently used blocks among the original 5.
- Once these 3 new blocks are loaded into the buffer, the buffer contains these 3 blocks and 2 of the old blocks. 
- Since the program now repeatedly accesses *only* these 3 new blocks, they become the most recently used. The 2 old blocks remain as the least recently used but are never replaced because no new blocks are being introduced.
- Therefore, no replacements occur during the repeated use of the first 5, and similarly, no replacements occur during the repeated use of the next 3. This matches description **b**.
