import httpx
from holehe.core import *
async def vinted(email, client, out):
    name, domain = "vinted", "vinted.com"
    try:
        h = {"User-Agent": "Vinted/2.0", "Accept": "application/json"}
        r = await client.post("https://www.vinted.com/api/v2/users/check_email", json={"email": email}, headers=h)
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.json().get("exists") == True})
    except: pass