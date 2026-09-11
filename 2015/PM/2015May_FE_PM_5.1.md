---
created: 2026-09-11 10:00
status: "#philnits"
tags:
  - algorithms
  - programming
  - software-testing
  - year/2015
---

# 2015May_FE_PM_5.1

![[2015May_FE_PM_Q5_Body_p1.png]]
![[2015May_FE_PM_Q5_Body_p2.png]]
![[2015May_FE_PM_Q5_Body_p3.png]]
?
d, a, e, c, a, d

### Explanation

**Blank A:**
In the original logic (`>` and `<`), when processing states for Highest Unemployment Rate, the variable `StateHigh` is only updated if `UnempRate > UnempRateHigh`. 
* **East:** 10.0 > 0.0 → Update `StateHigh = East`, `UnempRateHigh = 10.0`
* **North:** 10.0 > 10.0 → False, no update.
* **South:** 15.0 > 10.0 → Update `StateHigh = South`, `UnempRateHigh = 15.0`
* **West:** 15.0 > 15.0 → False, no update.
Thus, `StateHigh` ends up being **South** (`d`).

**Blank B:**
In Test Case 2, all states have a 0.0% unemployment rate. The initial value of `UnempRateHigh` is `0.0`.
For every state, the condition `0.0 > 0.0` is false. Therefore, `StateHigh` is never updated and retains its initial value of **"????"** (`a`).

**Blank C:**
In Test Case 3, the operators are changed to `>=` and `<=`, and all states have a 100.0% unemployment rate.
For every state, `UnempRate <= UnempRateLow` evaluates to `100.0 <= 100.0` (which is true). Because it is true for every state, `StateLow` continuously gets overwritten by the subsequent state. 
The last state processed is **West** (`e`), so `StateLow` becomes West.

**Blank D:**
In Test Case 4, with the operators still `>=` and `<=`, Test Case 1 is re-tested.
* **East:** 10.0 <= 100.0 → Update `StateLow = East`, `UnempRateLow = 10.0`
* **North:** 10.0 <= 10.0 → True, Update `StateLow = North`
* **South:** 15.0 <= 10.0 → False
* **West:** 15.0 <= 10.0 → False
The lowest unemployment rate variable `StateLow` stops updating at **North** (`c`).

**Blanks E and F:**
Instead of changing the operators, the issue in Test Case 2 (and its 100% counterpart) can be fixed by choosing initial values that are guaranteed to be surpassed by the very first record.
Since unemployment rates can only be between `0.0` and `100.0`:
* Initializing `UnempRateHigh` to **-0.1** (`a`) ensures that even a 0.0% rate will trigger the update (`0.0 > -0.1` is true).
* Initializing `UnempRateLow` to **100.1** (`d`) ensures that even a 100.0% rate will trigger the update (`100.0 < 100.1` is true).
