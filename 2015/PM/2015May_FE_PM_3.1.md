---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - networking
  - year/2015
---
# 2015May_FE_PM_3.1

![[2015May_FE_PM_Q3_Body_p1.png]]
![[2015May_FE_PM_Q3_Body_p2.png]]
![[2015May_FE_PM_Q3_SQ1_p1.png]]
![[2015May_FE_PM_Q3_SQ1_p2.png]]

?
c, d

### Explanation

**Blank A: Cabling or switch port problems**
According to the OSI Reference Model table, Layer 1 (Physical) and Layer 2 (Data Link) problems involve issues like "Cable unplug", "Cable defect", and "Network port malfunction". 
In Table 3 (Snapshot of the switch usage data), we look for interfaces experiencing physical link issues or frame errors:
*   **SW2 Port09 (User A):** Link status is "Down". This indicates a disconnected or broken cable, or a faulty port.
*   **SW3 Port12 (User D):** Frame CRC error is at 85%. High CRC (Cyclic Redundancy Check) errors strongly suggest a damaged cable or bad port, which corrupts frames during transmission.

Therefore, User A and User D have cabling or switch port problems. This corresponds to choice **c**.

**Blank B: MAC configuration problem**
A MAC configuration problem, as per the OSI table, involves "MAC address blocking" or "MAC level authentication".
Looking at Table 3 again for MAC filtering misconfigurations:
*   **SW3 Port01 (User C):** The recognized MAC is `CC:CC:CC:CC:CC:CC`. However, the MAC filter setting is configured to only `Allow: DD:DD:DD:DD:DD:DD`. Because the explicitly allowed MAC address does not match User C's actual MAC address, the switch will drop User C's frames.

Therefore, User C is the one experiencing a MAC configuration problem. This corresponds to choice **d**.
