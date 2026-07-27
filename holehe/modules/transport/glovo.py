import httpx
from holehe.core import *

async def glovo(email, client, out):
    name = "glovo"
    domain = "glovoapp.com"
    method = "register"
    f_out = []
    try:
        response = await client.post("https://glovoapp.com/api/v1/accounts/check", json={"email": email})
        if response.status_code == 409 or response.json().get("exists") is True:
            f_out.append({"name": name, "domain": domain, "method": method, "exists": True, "others": None})
        else:
            f_out.append({"name": name, "domain": domain, "method": method, "exists": False, "others": None})
    except Exception:
        f_out.append({"name": name, "domain": domain, "method": method, "exists": False, "others": "error"})
    out.extend(f_out)