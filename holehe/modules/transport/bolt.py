import httpx
from holehe.core import *

async def bolt(email, client, out):
    name = "bolt"
    domain = "bolt.eu"
    method = "register"
    f_out = []
    try:
        # Bolt требует специфические заголовки, имитируем мобильное приложение
        res = await client.post("https://bolt.eu/api/checkEmail", json={"email": email})
        if "already_exists" in res.text:
            f_out.append({"name": name, "domain": domain, "method": method, "exists": True, "others": None})
        else:
            f_out.append({"name": name, "domain": domain, "method": method, "exists": False, "others": None})
    except Exception:
        f_out.append({"name": name, "domain": domain, "method": method, "exists": False, "others": "error"})
    out.extend(f_out)