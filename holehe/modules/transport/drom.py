import httpx
from holehe.core import *
async def drom(email, client, out):
    name, domain = "drom", "drom.ru"
    try:
        r = await client.post("https://my.drom.ru/sign/checkLogin", data={"login": email})
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.json().get("status") == "exists"})
    except: pass