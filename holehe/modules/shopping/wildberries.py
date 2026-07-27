import httpx
from holehe.core import *

async def wildberries(email, client, out):
    name, domain = "wildberries", "wildberries.ru"
    try:
        headers = {
            "User-Agent": "Wildberries/5.4.2 (iPhone; iOS 16.0)",
            "X-Requested-With": "XMLHttpRequest"
        }
        r = await client.post("https://www.wildberries.ru/webapi/login/checkuser", data={"login": email}, headers=headers)
        if r.json().get("exists") == True:
            out.append({"name": name, "domain": domain, "method": "api", "exists": True})
        else:
            out.append({"name": name, "domain": domain, "method": "api", "exists": False})
    except:
        pass