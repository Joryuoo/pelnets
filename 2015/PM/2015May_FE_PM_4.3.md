---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - web-technologies
  - cybersecurity
  - year/2015
---
# 2015May_FE_PM_4.3

![[2015May_FE_PM_Q4_Body_p1.png]]
![[2015May_FE_PM_Q4_SQ3_p1.png]]
![[2015May_FE_PM_Q4_SQ3_p2.png]]

?
c

### Explanation
The question asks which tags caused the security message when browsing a secured page (`https://www.example.com/order`). This is a classic case of a **Mixed Content** warning. 

A mixed content warning occurs when a user visits a page accessed over a secure HTTPS connection, but the page includes resources (like images, scripts, or stylesheets) fetched over an insecure HTTP connection. Modern browsers block or warn users about these insecure requests because they can be intercepted or modified by attackers, compromising the security of the entire page.

Let's examine the resource links in the HTML source code:
* **(1)** `<link ... href="http://www.example.com/themes/main.css">` - Uses **HTTP**. This is insecure and causes a warning.
* **(2)** `<link ... href="http://www.example.com/themes/header.css">` - Uses **HTTP**. This is insecure and causes a warning.
* **(3)** `<script ... src="https://www.example.com/scripts/jquery.js"></script>` - Uses **HTTPS**. This is secure and does not cause a warning.
* **(4)** `<img src="http://www.example.com/images/shirt.jpg">` - Uses **HTTP**. This is insecure and causes a warning.

Tags (1), (2), and (4) are loaded over insecure HTTP connections, triggering the security message. Thus, the correct answer is **c**.

*   **Choice a is incorrect** because it includes tag (3), which is loaded securely over HTTPS, and omits tag (4).
*   **Choice b is incorrect** because it includes tag (3).
*   **Choice d is incorrect** because it includes tag (3) and omits tag (2).
