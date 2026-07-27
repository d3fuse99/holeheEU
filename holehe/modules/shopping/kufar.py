import httpx
from holehe.core import *
async def kufar(email, client, out):
    name, domain = "kufar", "kufar.by"
    try:
        r = await client.post("https://www.kufar.by/api/search/v1/user/check", json={"email": email})
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.json().get("exists") == True})
    except: pass