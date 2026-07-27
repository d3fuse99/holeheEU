import httpx
from holehe.core import *

async def dodopizza(email, client, out):
    name = "dodopizza"
    domain = "dodopizza.ru"
    method = "register"
    f_out = []
    try:
        # Проверка через API лояльности
        res = await client.get(f"https://globalapi.dodopizza.com/api/v1/customer/check?email={email}")
        if res.status_code == 200:
            f_out.append({"name": name, "domain": domain, "method": method, "exists": True, "others": None})
        else:
            f_out.append({"name": name, "domain": domain, "method": method, "exists": False, "others": None})
    except Exception:
        f_out.append({"name": name, "domain": domain, "method": method, "exists": False, "others": "error"})
    out.extend(f_out)