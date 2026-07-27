import httpx
from holehe.core import *
async def ozon(email, client, out):
    try:
        await client.get("https://www.ozon.ru/")
        h = {"User-Agent": "OzonAbra/1.0 (Android 12)"}
        r = await client.post("https://www.ozon.ru/api/composer-api.bx/v1/id/check-user", json={"email": email}, headers=h)
        out.append({"name": "ozon", "domain": "ozon.ru", "method": "api", "exists": r.json().get("userExists") == True})
    except: pass