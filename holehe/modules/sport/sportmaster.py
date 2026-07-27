import httpx
from holehe.core import *

async def sportmaster(email, client, out):
    name = "sportmaster"
    domain = "sportmaster.ru"
    method = "register"
    f_out = []
    try:
        res = await client.post("https://www.sportmaster.ru/api/v1/auth/checkEmail", json={"email": email})
        if res.json().get("exists") is True:
            f_out.append({"name": name, "domain": domain, "method": method, "exists": True, "others": None})
        else:
            f_out.append({"name": name, "domain": domain, "method": method, "exists": False, "others": None})
    except Exception:
        f_out.append({"name": name, "domain": domain, "method": method, "exists": False, "others": "error"})
    out.extend(f_out)