import httpx
from holehe.core import *
async def pornhub(email, client, out):
    try:
        await client.get("https://www.pornhub.com/register")
        r = await client.post("https://www.pornhub.com/user/check_email_all", data={"email": email}, headers={"X-Requested-With": "XMLHttpRequest"})
        if r.json().get("exists") == 1:
            out.append({"name": "pornhub", "domain": "pornhub.com", "method": "api", "exists": True})
        else:
            out.append({"name": "pornhub", "domain": "pornhub.com", "method": "api", "exists": False})
    except: pass