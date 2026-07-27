import httpx
from holehe.core import *
async def avito(email, client, out):
    try:
        h = {"User-Agent": "AvitoAndroid/13.8.1 (Android 14)", "X-Requested-With": "ru.avito.android"}
        r = await client.get(f"https://www.avito.ru/api/7/login/check_email?email={email}", headers=h)
        out.append({"name": "avito", "domain": "avito.ru", "method": "api", "exists": r.json().get("exists") == True})
    except: pass