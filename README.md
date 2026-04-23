# 🎯 Holehe: EU/CIS OSINT Edition

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![OSINT Focus](https://img.shields.io/badge/Focus-EU%20%2F%20CIS-red.svg)
![Status](https://img.shields.io/badge/Status-Optimized-green.svg)

An advanced **OSINT** (Open Source Intelligence) tool for checking email registrations across various services. This is a specialized fork of the original [Holehe](https://github.com/megadose/holehe), optimized specifically for the **European (EU)** and **CIS (Commonwealth of Independent States)** markets.

---

## ❓ Why this version?
Standard Holehe contains many obsolete or US-centric modules. This edition has been stripped of "bloatware" and upgraded with custom bypass logic for major Russian, Ukrainian, Kazakh, and European platforms.

### 🔥 Key Features
*   **📍 Regional Focus:** Optimized modules for *Wildberries, Ozon, Avito, Allegro, Vinted, Kaspi, Kufar*, and more.
*   **👤 Stealth (Deep) Mode:** Implements request jitter (random delays), connection limits, and mobile header rotation to bypass WAF.
*   **⚡ Real-time Reporting:** View results instantly as they are processed without waiting.
*   **📊 Visual Progress:** Integrated `tqdm` progress bar with live logging.
*   **🍪 Session Warming:** Pre-fetches cookies to mimic human behavior on high-security targets.

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/d3fuse99/HoleheEU.git
cd HoleheEU
2. Install dependencies
code
Bash
pip install trio httpx tqdm urllib3
🚀 Usage
The project includes a custom launcher check.py for easier access.
💨 Fast Scan
Quickly check all modules with standard settings.
code
Bash
python check.py target@email.com
🕵️‍♂️ Deep/Stealth Scan (Recommended)
Uses advanced bypass techniques to minimize LIMIT responses.
code
Bash
python check.py target@email.com d
📦 Supported Modules (48+)
Category	Services
✉️ Mails	Yandex, Mail.ru, Ukr.net, Rambler, Protonmail, Gmail, Yahoo
🛍️ Shopping	Wildberries, Ozon, Avito, Allegro (PL), Vinted (EU), Kaspi (KZ), Kufar (BY), Amazon
📱 Social	VK, Odnoklassniki, Pikabu, Facebook, Instagram, Twitter (X)
🚗 Transport	Bolt, Glovo, BlaBlaCar, Uber, Auto.ru
🎬 Medias	Megogo, Pornhub, Office365, Adobe, Duolingo, Twitch
⚙️ Technical Details
Async Engine: Trio (high-performance concurrent checking)
HTTP Client: HTTPX
Bypass: Mobile App API emulation & User-Agent rotation.
[!IMPORTANT]
Detection Rate & Limits: While optimized, some targets like Yandex or Avito may still return a LIMIT status if your IP is flagged. For a 100% success rate, change your IP address (e.g., using a mobile hotspot) between deep scans.
📜 Disclaimer
This tool is for educational and ethical research purposes only. The developers are not responsible for any misuse. Always ensure you have permission before conducting OSINT investigations.
🤝 Credits
Based on the original Holehe by Megadose.
Modified and improved by d3fuse99.
⭐ If you find this tool useful, please give it a star!
