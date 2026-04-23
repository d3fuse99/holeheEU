# Holehe: EU/CIS OSINT Edition

---

## About

**Holehe EU/CIS** is an advanced OSINT tool for checking email registrations across various services. 
Instead of checking obsolete US-centric modules — **real regional focus**: this specialized fork is optimized specifically for the European (EU) and CIS markets.

Built with custom bypass logic for major Russian, Ukrainian, Kazakh, and European platforms that are usually hard to probe due to strict anti-bot protections.

---

## Features

* **Regional Focus:** Optimized modules for Wildberries, Ozon, Avito, Allegro, Vinted, Kaspi, Kufar, Auto.ru, and more
* **48+ Supported Services** across Mails, Shopping, Social Media, Transport, and Adult categories
* **2 Scan Modes:** FAST / DEEP
* **Advanced bypass techniques:**
  * Request jitter (random delays) to simulate human behavior
  * Connection limits to prevent IP bans
  * Mobile User-Agent rotation and Mobile App API emulation
  * Session Warming (pre-fetches cookies and CSRF tokens)
* **Real-time Reporting:** View results instantly as they are processed without waiting
* **Visual Progress:** Integrated terminal progress bar with live logging

---

## How to run

1. Clone the repository: `git clone https://github.com/d3fuse99/HoleheEU.git`
2. Open the directory: `cd HoleheEU`
3. Install dependencies: `pip install trio httpx tqdm urllib3`
4. Run a fast scan: `python check.py target@email.com`
5. Run a deep/stealth scan: `python check.py target@email.com d`

**Note:** For a 100% success rate on high-security targets (Yandex, Avito, etc.), changing your IP address (e.g., using a mobile hotspot) between deep scans is highly recommended.

---

## Tech stack

* **Python 3.10+** — core language
* **Trio** — high-performance asynchronous I/O and concurrent checking
* **HTTPX** — modern HTTP client with HTTP/2 support
* **tqdm** — fast, extensible terminal progress bar

---

## Project structure
<img width="288" height="728" alt="image" src="https://github.com/user-attachments/assets/473abd8c-9f2d-4c51-b0f7-013f21ae6cca" />
