import httpx
from holehe.core import *
async def facebook(email, client, out):
    name, domain = "facebook", "facebook.com"
    try:
        r = await client.post("https://www.facebook.com/api/graphql/", data={"variables": f'{{"email":"{email}"}}', "doc_id": "5743444525738855"})
        out.append({"name": name, "domain": domain, "method": "api", "exists": "email_already_in_use" in r.text})
    except: pass