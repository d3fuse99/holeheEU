import httpx
from holehe.core import *
async def twitch(email, client, out):
    try:
        r = await client.post("https://passport.twitch.tv/register/check_email", json={"email": email})
        out.append({"name": "twitch", "domain": "twitch.tv", "method": "api", "exists": "taken" in r.text})
    except: pass