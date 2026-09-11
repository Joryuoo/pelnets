---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - cybersecurity
  - networking
  - year/2015
---
# 2015May_FE_PM_4.1

![[2015May_FE_PM_Q4_Body_p1.png]]
![[2015May_FE_PM_Q4_SQ1_p1.png]]
![[2015May_FE_PM_Q4_SQ1_p2.png]]

?
c, b, d

### Explanation
The HTTPS communication uses the SSL/TLS protocol to establish a secure connection. The initial phase to agree on keys and encryption methods is called the SSL handshake.

* **Blank A (Server to Client):** After the client (browser) initiates the connection and requests identification, the server responds by sending its digital certificate to the client. This certificate contains the server's public key and identity information. Therefore, **c) Server sends a copy of the SSL certificate to the browser** is the correct action for step (2).
* **Blank B (Client to Server):** Once the browser receives the certificate, it verifies the certificate's authenticity (checking if it was signed by a trusted Certificate Authority). After successful verification, it typically generates a session key (pre-master secret), encrypts it with the server's public key, and sends it to the server along with an acknowledgment message to switch to encrypted communication. Thus, **b) Browser verifies the certificate and sends an acknowledgment message to the server** fits step (3).
* **Blank C (Server to Client):** Finally, the server decrypts the session key using its private key and sends a final confirmation (Finished message) to the client. This matches **d) Server sends a digitally signed acknowledgement to the browser** for step (4).

**Why the other option is incorrect:**
* **a) Browser sends a copy of the SSL certificate to the server:** This describes client-side authentication, which is not part of the standard server-authentication HTTPS handshake described in this typical scenario.
