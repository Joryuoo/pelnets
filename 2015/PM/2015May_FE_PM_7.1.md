---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - programming
  - year/2015
---

# 2015May_FE_PM_7.1

![[2015May_FE_PM_Q7_Body_p1.png]]
![[2015May_FE_PM_Q7_SQ1_p1.png]]
![[2015May_FE_PM_Q7_SQ1_p2.png]]
![[2015May_FE_PM_Q7_SQ1_p3.png]]
![[2015May_FE_PM_Q7_SQ1_p4.png]]
![[2015May_FE_PM_Q7_SQ1_p5.png]]
![[2015May_FE_PM_Q7_SQ1_p6.png]]

?
a, a, c, b, b, c

### Explanation

**Blank A:** `a`
In the `deleted()` function, the program is deleting `n` characters from `source` starting at `index`. To accomplish this without losing the characters after the deleted portion, it first copies the characters after the deleted segment (`&source[index + n]`) into a temporary buffer `rest_str`. It then needs to copy this `rest_str` back into `source` starting at `index` to close the gap. Therefore, `strcpy(&source[index], rest_str)` is correct.
*   **b) strcpy(rest_str, &source[index])** is incorrect because it overwrites the temporary buffer instead of modifying the source string.
*   **c) and d)** are incorrect because `source[index]` is a `char` value, but `strcpy` expects a pointer (`char *`). This would cause a memory access violation or segmentation fault.

**Blank B:** `a`
In the `do_edit()` function under `case 'I'` (Insert), the program reads the string to insert (`str`) and the integer position (`index`). It then needs to call the `insert()` function to perform the operation. Looking at the definition `char * insert(char *source, const char *to_insert, int index)`, the arguments must be passed in the order: `source`, `str`, `index`. Thus, `insert(source, str, index)` is correct.
*   **b)** is incorrect because the order of arguments `(str, source, index)` would attempt to insert the source text into the temporary input buffer.
*   **c) and d)** are incorrect because `strcpy` merely copies one string over another and doesn't perform an insertion at a specific index.

**Blank C:** `c`
In the `do_edit()` function under `case 'F'` (Find), the program needs to find the position of the substring `str` within `source`. This is done using the `pos()` function, whose signature is `int pos(const char *source, const char *to_find)`. Calling `pos(source, str)` correctly maps the arguments.
*   **a) and b)** are incorrect because `*source` dereferences the pointer, yielding a single character. The function expects a pointer to a string.
*   **d)** is incorrect because the arguments are swapped; it would attempt to find `source` inside `str`.

**Blank D:** `b`
In the `insert()` function, the program needs to insert `to_insert` into `source` at `index`. To do this without overwriting the existing characters starting at `index`, it must first copy the remaining characters into `rest_str`. The characters to save begin at `&source[index]`. Therefore, `strcpy(rest_str, &source[index])` correctly saves the tail of the string.
*   **a)** is incorrect because `rest_str` is uninitialized at this point; this would overwrite the source with garbage data.
*   **c) and d)** are incorrect due to passing `char` instead of a `char *` pointer.

**Blank E:** `b`
In the `pos()` function, the program initializes variables to find a substring. The variable `find_len` is used heavily in the `while` loop condition (`i <= (int)strlen(source) - find_len`) and as the number of characters to copy (`strncpy`). It represents the length of the string being searched for. Thus, it must be initialized to `(int)strlen(to_find)`.
*   **a)** is incorrect because `find_len` should be the length of the substring to find, not the entire source string.
*   **c) and d)** are incorrect because `position` should not be assigned yet; it's determined after the loop finishes.

**Blank F:** `c`
In the `pos()` function, `strncpy(substring, &source[i], find_len)` is used to copy a chunk of characters into `substring`. However, `strncpy` does not automatically append a null terminator `'\0'` if the source is longer than or equal to the number of characters copied. To ensure `substring` is a properly terminated C string so that `strcmp(substring, to_find)` works correctly, we must manually append the null terminator at index `find_len`.
*   **a) and b)** are incorrect because they attempt to modify `source`, which is marked `const` and should not be changed by a find operation.
*   **d)** is incorrect because `'\n'` is a newline character, not a null terminator, so the string would remain unterminated.
