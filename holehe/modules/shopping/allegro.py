import httpx
from holehe.core import *
async def allegro(email, client, out):
    try:
        r = await client.post("https://allegro.pl/auth/login/check-email", json={"email": email})
        out.append({"name": "allegro", "domain": "allegro.pl", "method": "api", "exists": r.status_code == 409 or "taken" in r.text})
    except: pass