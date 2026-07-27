import httpx
from holehe.core import *
async def ukr_net(email, client, out):
    try:
        r = await client.post("https://accounts.ukr.net/registration/check-login", json={"login": email})
        out.append({"name": "ukr_net", "domain": "ukr.net", "method": "api", "exists": r.json().get("status") == "error"})
    except: pass