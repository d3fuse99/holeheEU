import httpx
from holehe.core import *
async def megogo(email, client, out):
    name, domain = "megogo", "megogo.net"
    try:
        r = await client.post("https://megogo.net/en/auth/check_login", data={"login": email})
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.json().get("successful") == False and "exists" in r.text})
    except: pass