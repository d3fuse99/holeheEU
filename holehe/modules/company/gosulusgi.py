import httpx
from holehe.core import *
async def gosuslugi(email, client, out):
    name, domain = "gosuslugi", "gosuslugi.ru"
    try:
        r = await client.post("https://esia.gosuslugi.ru/aas/oauth2/api/login", json={"login": email})
        out.append({"name": name, "domain": domain, "method": "api", "exists": "ID_NOT_FOUND" not in r.text})
    except: pass