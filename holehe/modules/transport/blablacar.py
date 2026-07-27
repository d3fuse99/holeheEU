import httpx
from holehe.core import *
async def blablacar(email, client, out):
    name, domain = "blablacar", "blablacar.com"
    try:
        r = await client.post("https://www.blablacar.com/api/proxy/v2/accounts/check-email", json={"email": email})
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.status_code == 409})
    except: pass