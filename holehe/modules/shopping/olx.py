import httpx
from holehe.core import *
async def olx(email, client, out):
    name, domain = "olx", "olx.ua"
    try:
        r = await client.get(f"https://www.olx.ua/api/v1/users/check-email/?email={email}")
        out.append({"name": name, "domain": domain, "method": "api", "exists": r.status_code == 409})
    except: pass