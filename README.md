# 🎯 Holehe: EU/CIS OSINT Edition

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![OSINT Focus](https://img.shields.io/badge/Focus-EU%20%2F%20CIS-red.svg)
![Status](https://img.shields.io/badge/Status-Optimized-green.svg)

An advanced **OSINT** (Open Source Intelligence) tool for checking email registrations across various services. This is a specialized fork of the original [Holehe](https://github.com/megadose/holehe), optimized specifically for the **European (EU)** and **CIS (Commonwealth of Independent States)** markets.

---

## ❓ Why this version?
Standard Holehe contains many obsolete or US-centric modules. This edition has been stripped of "bloatware" and upgraded with custom bypass logic for major Russian, Ukrainian, Kazakh, and European platforms.

### 🔥 Key Features
*   **📍 Regional Focus:** Optimized modules for *Wildberries, Ozon, Avito, Allegro, Vinted, Kaspi, Kufar, Auto.ru*, and more.
*   **👤 Stealth (Deep) Mode:** Implements request jitter (random delays), connection limits, and mobile header rotation to bypass WAF.
*   **⚡ Real-time Reporting:** View results instantly as they are processed without waiting for the entire scan to finish.
*   **📊 Visual Progress:** Integrated `tqdm` progress bar with live logging.
*   **🍪 Session Warming:** Pre-fetches cookies and CSRF tokens to mimic human behavior on high-security targets.

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/d3fuse99/HoleheEU.git
cd HoleheEU
