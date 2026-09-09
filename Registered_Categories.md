# Registered Flashcard Categories

This document lists all **30 officially registered topic categories** configured in the Obsidian Spaced Repetition plugin (`.obsidian/plugins/obsidian-spaced-repetition/data.json`).

> [!IMPORTANT]
> The Spaced Repetition plugin **strictly ignores any tag not in its registered settings list**. 
> Always use the registered category name (appended with the exam year, e.g. `cybersecurity/2025`) in the note's YAML frontmatter `tags:` list.

---

## Frontmatter Format

Every flashcard must include both the **category with the exam year** and the **year tag**:

```yaml
---
created: YYYY-MM-DD HH:mm
status: "#philnits"
tags:
  - appropriate-category/YYYY
  - year/YYYY
---
```

If a question spans multiple domains, you can include multiple registered categories:
```yaml
---
created: 2026-09-04 18:45
status: "#philnits"
tags:
  - artificial-intelligence/2026
  - algorithms/2026
  - year/2026
---
```

---

## Registered Categories Directory

| # | Category Tag | Scope & Key Concepts | Common Aliases / Mappings (Do NOT use as top tag) |
|---|---|---|---|
| 1 | `#accounting` | Balance sheets, profit calculation, P/L statements, break-even point, financial ratios. | `finance` |
| 2 | `#algorithms` | Sorting, searching, recursion, graph traversal, Euclidean GCD, algorithm complexity ($O(n)$). | `flowcharts` |
| 3 | `#artificial-intelligence` | Machine learning, deep learning, neural networks, NLP, LLMs, chatbots, computer vision. | `ai`, `ml`, `deep-learning` |
| 4 | `#automata-theory` | State machines, state transition diagrams, DFAs, NFAs, regular grammars. | `automata`, `state-transitions` |
| 5 | `#business-administration` | Business development, strategy, corporate governance, HR, procurement, contracts, BPR, TQM. | `management`, `business-strategy`, `corporate-strategy`, `hr` |
| 6 | `#cloud-computing` | IaaS, PaaS, SaaS, private/public/hybrid cloud, cloud architecture, multi-tenant systems. | `cloud`, `saas` |
| 7 | `#cybersecurity` | Information security, encryption (symmetric/asymmetric), hashes, malware, authentication, firewalls, CIA triad. | `security`, `network-security`, `cryptography` |
| 8 | `#data-encoding` | Compression (Huffman, Run-length), data representation, parity bits, check digits, character encoding (ASCII, UTF). | `compression`, `data-representation` |
| 9 | `#data-structures` | Stacks, queues, linked lists, binary trees, heaps, hash tables, graphs. | `stack`, `queue`, `tree` |
| 10 | `#devops` | CI/CD, automated provisioning, containerization (Docker, Kubernetes), infrastructure as code. | `containers`, `sysadmin` |
| 11 | `#digital-logic` | Boolean algebra, truth tables, Karnaugh maps, logic gates (AND, OR, NAND, XOR), flip-flops. | `logic-circuits`, `boolean-algebra` |
| 12 | `#hardware` | CPU architecture, memory hierarchy, cache, pipelining, interrupts, storage (HDD, SSD), RAID. | `computer-architecture`, `storage`, `raid` |
| 13 | `#information-management` | Databases, relational model, SQL queries, normalization (1NF-3NF), transactions, ACID properties, DBMS. | `database`, `sql`, `dbms` |
| 14 | `#math` | Arithmetic, linear equations, matrices, basic algebra word problems, set-based calculations. | `algebra`, `arithmetic` |
| 15 | `#networking` | OSI 7 layers, TCP/IP, IP addressing, subnetting, CIDR, routing protocols, DNS, ARP, HTTP, Wi-Fi. | `network`, `osi-model`, `routing`, `tcp-ip` |
| 16 | `#number-systems` | Conversions between binary, octal, decimal, and hexadecimal; IEEE 754 floating-point; two's complement. | `binary`, `hexadecimal`, `floating-point` |
| 17 | `#object-oriented-programming` | Classes, objects, inheritance, polymorphism, encapsulation, method overriding, overloading, abstract classes. | `oop`, `classes` |
| 18 | `#operating-systems` | CPU scheduling algorithms, virtual memory, paging, thrashing, deadlocks, process management, file systems. | `os`, `cpu-scheduling`, `memory-management` |
| 19 | `#probability` | Independent events, conditional probability, Bayes' theorem, permutations, combinations, queuing theory ($M/M/1$). | `queuing-theory`, `combinatorics` |
| 20 | `#programming` | Variables, loops, scoping, pointers, syntax, data types, parameter passing, compiler stages. | `coding`, `compilation` |
| 21 | `#project-management` | Scrum, Agile, Waterfall, Gantt charts, CPM / PERT, critical path, WBS, EVM, risk management. | `pm`, `agile`, `scrum` |
| 22 | `#service-management` | ITIL, SLA, incident management, change management, availability management, service reliability. | `itil`, `sla`, `system-reliability` |
| 23 | `#sets` | Set operations (union, intersection, complement), Venn diagrams, Cartesian products. | `venn-diagrams`, `set-theory` |
| 24 | `#software` | General software tools, utilities, graphics software, presentation software, desktop applications. | `tools`, `applications` |
| 25 | `#software-engineering` | Software development lifecycle (SDLC), design patterns, UML diagrams, requirements engineering, CMMI. | `uml`, `design-patterns`, `system-design` |
| 26 | `#software-testing` | Unit testing, integration testing, system testing, black-box / white-box testing, boundary value analysis. | `testing`, `qa`, `tdd` |
| 27 | `#statistics` | Mean, median, mode, standard deviation, normal distribution, correlation, regression analysis. | `regression`, `standard-deviation` |
| 28 | `#systems-architecture` | System topologies, client-server, microservices, system availability calculation ($R = 1 - (1-r)^2$), fault tolerance. | `system-architecture`, `reliability` |
| 29 | `#web-technologies` | HTML, CSS, JavaScript, DOM, REST APIs, JSON, AJAX, web cookies, sessions. | `web`, `frontend`, `apis` |
| 30 | `#year` | Special organizational tag used to group all exam questions for a specific year (e.g. `#year/2025`). | (Do not omit from cards) |

---

## Tag Mapping Reference Guide

When writing or importing new questions, **map informal tags to the official registered categories**:

| When the topic is... | DO NOT tag with... | USE THIS REGISTERED TAG |
|---|---|---|
| Cybersecurity / InfoSec | `security`, `network-security`, `cryptography` | `cybersecurity` |
| Networking / Protocols | `network`, `osi-model`, `routing`, `ip`, `tools` | `networking` |
| Databases & SQL | `database`, `sql`, `dbms`, `relational-database` | `information-management` |
| Computer Architecture & Disks | `computer-architecture`, `storage`, `raid` | `hardware` |
| Management, Strategy & HR | `management`, `business-strategy`, `corporate-strategy`, `hr`, `marketing` | `business-administration` |
| AI, ML & Deep Learning | `ai`, `ml`, `deep-learning` | `artificial-intelligence` |
| Cloud Services (IaaS/PaaS/SaaS) | `cloud`, `saas` | `cloud-computing` |
| Object-Oriented Concepts | `oop` | `object-oriented-programming` |
| Logic Gates & Circuits | `logic-circuits` | `digital-logic` |
| Software Architecture & UML | `system-architecture`, `uml`, `system-design` | `software-engineering` or `systems-architecture` |
| Memory & CPU Scheduling | `memory-management`, `cpu-scheduling` | `operating-systems` |
| Queuing Models ($M/M/1$) | `queuing-theory` | `probability` |
| Data Encoding & Parity | `data-representation`, `check-digit` | `data-encoding` |
