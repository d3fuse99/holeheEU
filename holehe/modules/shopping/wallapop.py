import httpx
from holehe.core import *
async def wallapop(email, client, out):
    try:
        r = await client.get(f"https://api.wallapop.com/api/v3/users/check?email={email}")
        out.append({"name": "wallapop", "domain": "wallapop.com", "method": "api", "exists": r.status_code == 409})
    except: pass