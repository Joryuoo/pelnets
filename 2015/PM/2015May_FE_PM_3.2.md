---
created: 2026-09-11 09:59
status: "#philnits"
tags:
  - networking
  - year/2015
---
# 2015May_FE_PM_3.2

![[2015May_FE_PM_Q3_SQ2_p1.png]]
![[2015May_FE_PM_Q3_SQ2_p2.png]]

?
b, c

### Explanation

**Blank C:**
User F's PC is assigned the IP address `10.10.2.55`. According to the network configuration in the scenario, the PC is connected to Switch 3 (SW3), which connects to the internet access router via interface **R2**. The IP address of R2 is given as `10.10.2.254`. 
For the PC to communicate with devices outside its local subnet (such as the Intranet on different subnets or the Internet), it must forward those IP packets to its default gateway. A default gateway route is specified with a destination of `0.0.0.0` and a netmask of `0.0.0.0`. The gateway IP address must be the router interface on the PC's local subnet, which is `10.10.2.254`.
Therefore, the correct routing record is Destination: `0.0.0.0`, Netmask: `0.0.0.0`, Gateway: `10.10.2.254`, which corresponds to choice **b**.

*Why other choices are incorrect:*
- **a:** Uses gateway `10.10.1.254` (R1), which is on a different subnet and unreachable directly by User F's PC.
- **c:** Uses gateway `202.170.10.1` (R3), the external internet interface, also unreachable directly.
- **d, e, f:** These specify specific subnet destinations rather than the `0.0.0.0` catch-all default route needed to access *both* the Intranet and the Internet.

**Blank D:**
DNS (Domain Name System) is responsible for resolving domain names (like `http://www.itpec.org`) into their corresponding IP addresses (`64.22.66.88`). 
If there is a DNS misconfiguration, the PC will fail to resolve the domain name, making the URL `http://www.itpec.org` inaccessible. However, accessing the website directly via its IP address `http://64.22.66.88` bypasses the DNS resolution process. Because Layers 1-3 are already confirmed to be working, the direct IP request will succeed.
Therefore, a DNS problem is confirmed when the domain name is inaccessible but the IP address is accessible, which corresponds to choice **c**.

*Why other choices are incorrect:*
- **a:** Both being accessible means DNS and routing are working perfectly.
- **b:** Domain accessible but IP inaccessible is unlikely in a standard network troubleshooting scenario, as domain resolution implies IP access should work.
- **d:** Both being inaccessible suggests a deeper issue such as a routing failure, firewall block, or the web server itself being down, rather than just a DNS misconfiguration.
