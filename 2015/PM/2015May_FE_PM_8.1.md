---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - programming
  - object-oriented-programming
  - year/2015
---

# 2015May_FE_PM_8.1

![[2015May_FE_PM_Q8_Body_p1.png]]
![[2015May_FE_PM_Q8_Body_p2.png]]
![[2015May_FE_PM_Q8_Body_p3.png]]
![[2015May_FE_PM_Q8_Body_p4.png]]
![[2015May_FE_PM_Q8_Body_p5.png]]
![[2015May_FE_PM_Q8_Body_p6.png]]
![[2015May_FE_PM_Q8_Body_p7.png]]

?
A=d, B=f, C=h, D=a, E=c (Note: Answers for A and B can be exchanged)

### Explanation

**Blank A:** `d) Comparable<Player>`
The `Player` class contains an overridden `compareTo(Player p)` method. In Java, to sort objects natively (such as with `Collections.sort()`), the class must implement the `Comparable` interface. Since it's comparing with other `Player` objects, the generic type is `<Player>`. 

**Blank B:** `f) public abstract`
In `Program 3`, the `Game` class implements the `GameLoop` interface but does not provide implementations for `startGame()`, `playGame()`, and `endGame()`. Because it leaves these methods unimplemented for its subclasses (like `RoPaScGame`) to define, the `Game` class itself must be declared as `abstract`. It also needs to be `public` so it can be instantiated in other parts of the application.

**Blank C:** `h) public static`
In `Program 6` (line 254), the `checkWinner` method is called directly on the `GameLogic` class itself without creating an instance: `GameLogic.checkWinner(player,computer)`. Therefore, `checkWinner` must be a `static` method. It also needs to be `public` to be accessed from outside its class.

**Blank D:** `a) Math.abs(player1.getChoice() - player2.getChoice())`
The choices are mapped as: Rock = 0, Paper = 1, Scissors = 2.
Winning conditions are:
- Paper (1) beats Rock (0) -> difference is 1 (larger wins)
- Scissors (2) beats Paper (1) -> difference is 1 (larger wins)
- Rock (0) beats Scissors (2) -> difference is 2 (smaller wins)

The code checks if `player1.getChoice() < player2.getChoice()`. If their absolute difference is `1`, `player2` (the larger value) wins. If the absolute difference is `2` (meaning a 0 vs 2 scenario), `player1` (the smaller value, Rock) wins. Thus, `Math.abs(...)` correctly captures this logic.

**Blank E:** `c) Collections`
In `Program 6` (line 261), the `players` list needs to be sorted based on their scores. In Java, the utility class `Collections` provides the `sort()` static method for sorting `List` objects. Hence, `Collections.sort(players)` is the correct statement.
