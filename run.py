import trio
import httpx
import sys
import urllib3
import random
import os
import json
import csv
import webbrowser
import re
from holehe.core import import_submodules
from tqdm import tqdm

urllib3.disable_warnings()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Build/UQ1A.231205.015) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

def log_error(module_name, error_msg):
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "error_log.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{module_name}] {error_msg}\n")

def export_results(out, format_type):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if format_type == "json":
        file_path = os.path.join(base_dir, "results.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=4, ensure_ascii=False)
        print(f"Results exported to {file_path}")
    elif format_type == "csv":
        file_path = os.path.join(base_dir, "results.csv")
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Domain", "Method", "Exists"])
            for r in out:
                writer.writerow([r.get("name"), r.get("domain"), r.get("method"), r.get("exists")])
        print(f"Results exported to {file_path}")

def export_html(email, html_results):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "results.html")
    
    total = len(html_results)
    exists = sum(1 for r in html_results if r["status"] == "EXISTS")
    not_found = sum(1 for r in html_results if r["status"] == "not found")
    limits = sum(1 for r in html_results if r["status"] in ["LIMIT", "ERROR"])
    
    cards_html = ""
    for r in html_results:
        status = r["status"]
        name = r["name"]
        domain = r["domain"]
        
        if status == "EXISTS":
            bg_color = "bg-zinc-950 border-emerald-500/10 hover:border-emerald-500/60 shadow-[0_0_15px_rgba(16,185,129,0.02)] hover:shadow-[0_0_20px_rgba(16,185,129,0.15)]"
            text_color = "text-emerald-500"
            badge = """
            <span class="px-2 py-1 text-[11px] font-bold rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
                <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span data-card-status="EXISTS">НАЙДЕН</span>
            </span>
            """
        elif status == "not found":
            bg_color = "bg-zinc-950 border-zinc-900 hover:border-zinc-700 shadow-[0_0_15px_rgba(255,255,255,0.01)] hover:shadow-[0_0_20px_rgba(255,255,255,0.05)]"
            text_color = "text-zinc-500"
            badge = """
            <span class="px-2 py-1 text-[11px] font-bold rounded-lg bg-zinc-900/60 text-zinc-400 border border-zinc-800 flex items-center gap-1.5">
                <span class="inline-flex rounded-full h-2 w-2 bg-zinc-600"></span>
                <span data-card-status="not found">Не найден</span>
            </span>
            """
        elif status == "LIMIT":
            bg_color = "bg-zinc-950 border-amber-500/10 hover:border-amber-500/60 shadow-[0_0_15px_rgba(245,158,11,0.02)] hover:shadow-[0_0_20px_rgba(245,158,11,0.15)]"
            text_color = "text-amber-500"
            badge = """
            <span class="px-2 py-1 text-[11px] font-bold rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center gap-1.5">
                <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
                </span>
                <span data-card-status="statusLimit">Лимит</span>
            </span>
            """
        else:
            bg_color = "bg-zinc-950 border-rose-500/10 hover:border-rose-500/60 shadow-[0_0_15px_rgba(239,68,68,0.02)] hover:shadow-[0_0_20px_rgba(239,68,68,0.15)]"
            text_color = "text-rose-500"
            badge = """
            <span class="px-2 py-1 text-[11px] font-bold rounded-lg bg-rose-500/10 text-rose-400 border border-rose-500/20 flex items-center gap-1.5">
                <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
                </span>
                <span data-card-status="statusError">Ошибка</span>
            </span>
            """
            
        cards_html += f"""
        <div class="result-card p-5 rounded-2xl border {bg_color} transition-all duration-300 hover:-translate-y-1 transform" data-status="{status}" data-name="{name}">
            <div class="flex items-center justify-between mb-3">
                <h3 class="text-base font-extrabold text-zinc-100 tracking-tight">{name}</h3>
                {badge}
            </div>
            <p class="text-xs {text_color} break-all font-mono">
                <i class="fa-solid fa-link mr-1 opacity-70"></i> {domain}
            </p>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holehe OSINT Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{
            background-color: rgb(0, 0, 0);
        }}
    </style>
</head>
<body class="text-zinc-200 font-sans min-h-screen selection:bg-indigo-500 selection:text-white antialiased">
    <div class="max-w-7xl mx-auto px-4 py-12">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between border-b border-zinc-900 pb-8 mb-10 gap-4">
            <div>
                <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent flex items-center gap-2">
                    <i class="fa-solid fa-circle-nodes"></i> Holehe: EU/CIS OSINT
                </h1>
                <p class="text-slate-400 mt-1">Отчет сканирования для адреса: <span class="text-indigo-400 font-semibold">{email}</span></p>
            </div>
            <div class="flex items-center gap-3">
                <div class="relative">
                    <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </span>
                    <input type="text" id="search-input" onkeyup="searchSite()" placeholder="Поиск сервиса..." 
                           class="bg-slate-900 text-slate-200 pl-10 pr-4 py-2 rounded-lg border border-slate-800 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 w-64 transition">
                </div>
            </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div onclick="filterResults('all')" class="bg-slate-900 border border-slate-800 p-4 rounded-xl cursor-pointer hover:border-indigo-500/50 transition">
                <div class="text-sm text-slate-400">Всего проверено</div>
                <div class="text-2xl font-bold mt-1 text-slate-200">{total}</div>
            </div>
            <div onclick="filterResults('EXISTS')" class="bg-slate-900 border border-slate-800 p-4 rounded-xl cursor-pointer hover:border-green-500/50 transition">
                <div class="text-sm text-green-400">Найдено аккаунтов</div>
                <div class="text-2xl font-bold mt-1 text-green-400">{exists}</div>
            </div>
            <div onclick="filterResults('not found')" class="bg-slate-900 border border-slate-800 p-4 rounded-xl cursor-pointer hover:border-slate-500/50 transition">
                <div class="text-sm text-slate-400">Не найдено</div>
                <div class="text-2xl font-bold mt-1 text-slate-400">{not_found}</div>
            </div>
            <div onclick="filterResults('LIMIT')" class="bg-slate-900 border border-slate-800 p-4 rounded-xl cursor-pointer hover:border-amber-500/50 transition">
                <div class="text-sm text-amber-400">Лимит/Ошибки</div>
                <div class="text-2xl font-bold mt-1 text-amber-400">{limits}</div>
            </div>
        </div>

        <div class="flex flex-wrap gap-2 mb-6">
            <button onclick="filterResults('all')" class="px-4 py-1.5 rounded-lg text-sm font-medium bg-slate-900 hover:bg-slate-800 border border-slate-800 transition">Все</button>
            <button onclick="filterResults('EXISTS')" class="px-4 py-1.5 rounded-lg text-sm font-medium bg-green-950/40 hover:bg-green-900/40 border border-green-500/30 text-green-400 transition">Найденные</button>
            <button onclick="filterResults('not found')" class="px-4 py-1.5 rounded-lg text-sm font-medium bg-slate-900/60 hover:bg-slate-800/60 border border-slate-700/30 text-slate-400 transition">Не найденные</button>
            <button onclick="filterResults('LIMIT')" class="px-4 py-1.5 rounded-lg text-sm font-medium bg-amber-950/40 hover:bg-amber-900/40 border border-amber-500/30 text-amber-400 transition">Лимиты</button>
        </div>

        <div id="results-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {cards_html}
        </div>
    </div>

    <script>
        function filterResults(type) {{
            const cards = document.querySelectorAll('.result-card');
            cards.forEach(card => {{
                if (type === 'all') {{
                    card.style.display = 'block';
                }} else if (type === 'LIMIT') {{
                    if (card.dataset.status === 'LIMIT' || card.dataset.status === 'ERROR') {{
                        card.style.display = 'block';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }} else {{
                    if (card.dataset.status === type) {{
                        card.style.display = 'block';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }}
            }});
        }}

        function searchSite() {{
            const query = document.getElementById('search-input').value.toLowerCase();
            const cards = document.querySelectorAll('.result-card');
            cards.forEach(card => {{
                const name = card.dataset.name.toLowerCase();
                if (name.includes(query)) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>
"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\n[*] HTML report successfully created: {file_path}")
    if os.environ.get("HOLEHE_WEB") != "1":
        webbrowser.open(f"file://{os.path.abspath(file_path)}")

async def safe_check(func, email, client, out, html_results, mode, pbar):
    module_name = func.__name__
    try:
        t_limit = 35 if mode == "deep" else 15
        await trio.sleep(random.uniform(0.1, 0.5))

        with trio.move_on_after(t_limit):
            await func(email, client, out)
        
        res = next((item for item in reversed(out) if item['name'] == module_name), None)
        status = "[+]" if res and res['exists'] else "[-]" if res else "[L]"
        label = "EXISTS" if status == "[+]" else "not found" if status == "[-]" else "LIMIT"
        domain = res["domain"] if res else "N/A"

        pbar.write(f"{status} {module_name:<15} | {label} | {domain}")
        pbar.update(1)
        
        html_results.append({
            "name": module_name,
            "status": label,
            "domain": domain
        })
    except Exception as e:
        log_error(module_name, str(e))
        pbar.write(f"[L] {module_name:<15} | LIMIT | N/A")
        pbar.update(1)
        html_results.append({
            "name": module_name,
            "status": "LIMIT",
            "domain": "N/A"
        })

def validate_email_syntax(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

async def check_domain_exists(email: str) -> bool:
    try:
        domain = email.split("@")[-1]
        await trio.socket.getaddrinfo(domain, None)
        return True
    except Exception:
        return False

async def check_email(email, mode, export_type):
    if not validate_email_syntax(email):
        print(f"\n[!] Error: Invalid email format '{email}'")
        return

    print(f"\n[*] Checking if domain exists for {email}...")
    domain_exists = await check_domain_exists(email)
    if not domain_exists:
        print(f"[!] Error: The domain '{email.split('@')[-1]}' does not exist or is unreachable.")
        return

    out = []
    html_results = []
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,uk;q=0.7',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.google.com/'
    }
    
    conn_limit = 5 if mode == "deep" else 15
    async with httpx.AsyncClient(headers=headers, verify=False, timeout=25, limits=httpx.Limits(max_connections=conn_limit)) as client:
        print(f"\n--- TARGET: {email} | MODE: {mode.upper()} ---\n")
        
        try:
            modules_dict = import_submodules("holehe.modules")
        except Exception as e:
            print(f"Error loading modules: {e}")
            return

        all_funcs = [getattr(obj, name.split(".")[-1]) for name, obj in modules_dict.items() if hasattr(obj, name.split(".")[-1])]

        with tqdm(total=len(all_funcs), desc="Scanning", unit="site", colour="green") as pbar:
            async with trio.open_nursery() as nursery:
                for func in all_funcs:
                    nursery.start_soon(safe_check, func, email, client, out, html_results, mode, pbar)

    print("\n" + "="*45 + "\nFINAL REPORT:")
    found = [r for r in out if r.get('exists')]
    for r in found:
        print(f"[+] {r['name']:<15} | {r['domain']}")
    if not found:
        print("No accounts found.")
    print("="*45)

    if export_type in ["json", "csv"]:
        export_results(out, export_type)
        
    export_html(email, html_results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py email [d] [json/csv]")
        sys.exit()
    
    email = sys.argv[1]
    mode = "fast"
    export_type = "none"
    
    for arg in sys.argv[2:]:
        if arg == "d":
            mode = "deep"
        elif arg in ["json", "csv"]:
            export_type = arg
            
    trio.run(check_email, email, mode, export_type)