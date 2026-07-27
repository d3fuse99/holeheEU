import httpx
from holehe.core import *
async def vk(email, client, out):
    try:
        r = await client.get(f"https://vk.com/auth?act=auth_by_password&email={email}")
        if any(x in r.text for x in ["email_is_taken", "has_account"]):
            out.append({"name": "vk", "domain": "vk.com", "method": "api", "exists": True})
    except: pass