import httpx
from holehe.core import *
async def habr(email, client, out):
    name, domain = "habr", "habr.com"
    try:
        r = await client.post("https://habr.com/kek/v1/auth/check-email", json={"email": email})
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.json().get("exists") == True})
    except: pass