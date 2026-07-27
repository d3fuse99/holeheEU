import httpx
from holehe.core import *
async def kaspi(email, client, out):
    name, domain = "kaspi", "kaspi.kz"
    try:
        h = {"Referer": "https://kaspi.kz/yml/registration"}
        r = await client.post("https://kaspi.kz/yml/registration/check-login", data={"login": email}, headers=h)
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.json().get("status") == "exists"})
    except: pass