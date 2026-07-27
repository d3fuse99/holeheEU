<div align="center">
  <h1>Holehe OSINT Web Interface</h1>
  <p>Modern, high-performance web dashboard for checking email registrations across 50+ online platforms in real-time.</p>
</div>

<h2>Overview</h2>
<p>Holehe OSINT Web is a fast, responsive web application wrapper built on top of FastAPI and Holehe Core. It queries public registration and password recovery endpoints to analyze online digital footprints without saving or storing private user data.</p>

<h2>Key Features</h2>
<ul>
  <li><b>Real-Time SSE Streaming</b>: Live progress updating card-by-card as checks complete.</li>
  <li><b>Smart Email Provider Detection</b>: Auto-detects Google, Yandex, Mail.ru, Proton, Microsoft, and Apple domains.</li>
  <li><b>Interactive Filtering & Search</b>: Instant live search by service name and category tabs (All, Found, Not Found, Rate Limits).</li>
  <li><b>Multi-Language Support</b>: Full Russian (RU) and English (EN) localization switcher.</li>
  <li><b>Custom Day/Night Theme Slider</b>: Dynamic sky theme transition engine with custom CSS animations.</li>
  <li><b>Multiple Export Formats</b>: Download report as .TXT or .JSON, or copy all found accounts in one click.</li>
</ul>

<h2>Tech Stack</h2>
<ul>
  <li><b>Backend</b>: Python 3, FastAPI, Asyncio, Trio, HTTPX</li>
  <li><b>Frontend</b>: JavaScript (ES6), HTML5, Tailwind CSS, FontAwesome</li>
  <li><b>Engine</b>: Holehe OSINT Core</li>
</ul>

<h2>Installation & Local Run</h2>
<pre>
git clone https://github.com/d3fuse99/holeheEU.git
cd holeheEU
pip install -r requirements.txt
python web/server.py
</pre>

<h2>License</h2>
<p>Distributed under the <b>GNU General Public License v3.0 (GPL-3.0)</b>.</p>
