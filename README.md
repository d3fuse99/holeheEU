An advanced OSINT (Open Source Intelligence) tool for checking email registrations across various services. This is a specialized fork of the original Holehe, optimized specifically for the European (EU) and CIS (Commonwealth of Independent States) markets.
⚠️ Why this version?
Standard Holehe contains many obsolete or US-centric modules. This edition has been stripped of "bloatware" and upgraded with custom bypass logic for major Russian, Ukrainian, Kazakh, and European platforms that are usually hard to probe due to anti-bot protections.
🔥 Key Features
Regional Focus: Optimized modules for Wildberries, Ozon, Avito, Allegro, Vinted, Kaspi, Kufar, and more.
Stealth (Deep) Mode: Implements request jitter (random delays), connection limits, and mobile header rotation to bypass WAF (Web Application Firewalls).
Real-time Reporting: View results instantly as they are processed without waiting for the entire scan to finish.
Visual Progress: Integrated tqdm progress bar with live logging.
Session Warming: Pre-fetches cookies and CSRF tokens to mimic human behavior on high-security targets (Yandex, Mail.ru, etc.).
🛠 Installation
Clone the repository:
code
Bash
git clone https://github.com/yourusername/holehe-eu-cis.git
cd holehe-eu-cis
Install dependencies:
code
Bash
pip install trio httpx tqdm urllib3
🚀 Usage
The project includes a custom launcher check.py for easier access.
1. Fast Scan
Quickly check all modules with standard settings.
code
Bash
python check.py target@email.com
2. Deep/Stealth Scan (Recommended)
Uses advanced bypass techniques, connection limits, and random delays to minimize LIMIT responses.
code
Bash
python check.py target@email.com d
📊 Supported Modules (48+)
This version covers the most critical services in EU and CIS:
Mails: Yandex, Mail.ru, Ukr.net, Rambler, Protonmail, Gmail, Yahoo.
Shopping: Wildberries, Ozon, Avito, Allegro (PL), Vinted (EU), Kaspi (KZ), Kufar (BY), Wallapop (ES/FR), Amazon.
Social: VK, Odnoklassniki, Pikabu, Facebook, Instagram, Twitter (X).
Transport: Bolt, Glovo, BlaBlaCar, Uber, Auto.ru.
Medias/Others: Megogo, Pornhub, Office365, Adobe, Duolingo, Twitch, and more.
⚙️ Technical Details
Language: Python 3.10+
Async Engine: Trio (for high-performance concurrent checking)
HTTP Client: HTTPX (with HTTP/2 support)
Bypass Methods:
Mobile App API emulation.
Custom User-Agent rotation.
Intelligent retry logic for LIMIT status.
📈 Detection Rate & Limits
While this tool is highly optimized, some high-security targets (like Yandex or Avito) may still return a LIMIT status if your IP address is flagged.
Pro Tip: For 100% success rate, it is recommended to change your IP address (e.g., using a mobile hotspot/LTE) between deep scans.
📜 Disclaimer
This tool is for educational and ethical security research purposes only. The developers are not responsible for any misuse or damage caused by this program. Always ensure you have permission before conducting OSINT investigations.
🤝 Credits
Based on the original Holehe by Megadose.
Modified and improved for regional OSINT by d3fuse99.
⭐ Support
If you find this tool useful, please give it a star on GitHub!
