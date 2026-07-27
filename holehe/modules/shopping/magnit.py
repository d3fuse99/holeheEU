import httpx
from holehe.core import *
async def magnit(email, client, out):
    name, domain = "magnit", "magnit.ru"
    try:
        r = await client.post("https://magnit.ru/api/v1/auth/check/", json={"login": email})
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.json().get("exists") == True})
    except: pass