import httpx
from holehe.core import *

async def steam(email, client, out):
    name, domain = "steam", "steampowered.com"
    try:
        await client.get("https://store.steampowered.com/join/", timeout=10)
        
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://store.steampowered.com/join/",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
        r = await client.post(
            "https://store.steampowered.com/join/ajaxcheckemail/",
            data={"email": email, "count": "1"},
            headers=headers
        )
        
        res = r.json()
        if res.get("success") == 2:
            out.append({"name": name, "domain": domain, "method": "api", "exists": True})
        else:
            out.append({"name": name, "domain": domain, "method": "api", "exists": False})
    except:
        pass