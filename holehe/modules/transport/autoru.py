import httpx
from holehe.core import *
async def autoru(email, client, out):
    name, domain = "autoru", "auto.ru"
    try:
        r = await client.post("https://auto.ru/api/1.0/auth/login-check", json={"login": email})
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.json().get("status") == "SUCCESS"})
    except: pass