import httpx
from holehe.core import *
async def yandex(email, client, out):
    try:
        h = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)", "Referer": "https://passport.yandex.ru/"}
        r = await client.get(f"https://passport.yandex.ru/registration-validations/check?login={email}", headers=h)
        out.append({"name": "yandex", "domain": "yandex.ru", "method": "api", "exists": "account_is_taken" in r.text})
    except: pass