import httpx
from holehe.core import *
async def mail_ru(email, client, out):
    try:
        await client.get("https://mail.ru/")
        h = {"X-Requested-With": "ru.mail.mailapp", "User-Agent": "Mail.ruApp/14.10.0"}
        r = await client.post("https://account.mail.ru/api/v1/user/exists", data={"email": email}, headers=h)
        out.append({"name": "mail_ru", "domain": "mail.ru", "method": "api", "exists": r.json().get("body", {}).get("exists") == True})
    except: pass