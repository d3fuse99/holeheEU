import httpx
from holehe.core import *
async def hh_ru(email, client, out):
    name, domain = "hh_ru", "hh.ru"
    try:
        r = await client.post("https://hh.ru/oauth/password_recovery", data={"login": email})
        out.append({"name": name, "domain": domain, "method": "api", "exists": "не найден" not in r.text and r.status_code == 200})
    except: pass