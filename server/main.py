import os
import json
import httpx
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from jose import jwt
from urllib.request import urlopen

# Import the vault we made in Phase 5
from vault import vault 

load_dotenv()
app = FastAPI(title="Aegis-MCP Secure Proxy")

# --- CONFIG ---
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_INTERNAL_API_AUDIENCE")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
TARGET_USER_ID = "auth0|69cea7cadd48ff21b478f784"

# --- PHASE 2: THE SHIELD (JWT Verification) ---
def verify_jwt(token: str):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}
    if rsa_key:
        payload = jwt.decode(token, rsa_key, algorithms=["RS256"], audience=API_AUDIENCE, issuer=f"https://{AUTH0_DOMAIN}/")
        return payload
    raise Exception("Cryptographic key mismatch.")

# --- PHASE 3: IDENTITY PROXY MIDDLEWARE ---
@app.middleware("http")
async def identity_aware_proxy(request: Request, call_next):
    if request.url.path in ["/health", "/"]:
        return await call_next(request)
        
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        print("[SHIELD] Blocked: Missing Token.")
        return JSONResponse(status_code=401, content={"detail": "Aegis Protocol: Missing Token."})
        
    try:
        token = auth_header.split(" ")[1]
        request.state.user = verify_jwt(token)
        print("[SHIELD] Traffic cleared. Identity verified.")
    except Exception as e:
        print(f"[SHIELD] Blocked: {str(e)}")
        return JSONResponse(status_code=401, content={"detail": f"Access Denied: {str(e)}"})

    return await call_next(request)

# --- PHASE 4 & 5: CIBA + VAULT ---
@app.post("/agent/execute-high-stakes")
async def execute_high_stakes_action(request: Request):
    print("[AEGIS-MCP] High-stakes action detected. Pausing thread...")

    # 1. Fire CIBA (Using your successful 'Bingo' format)
    ciba_url = f"https://{AUTH0_DOMAIN}/bc-authorize"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "openid profile email write:finance",
        "binding_message": "Aegis Approve transaction for Stripe",
        "login_hint": json.dumps({
            "format": "iss_sub",  
            "iss": f"https://{AUTH0_DOMAIN}/",
            "sub": TARGET_USER_ID
        })
    }
                                                                   
    async with httpx.AsyncClient() as client:
        response = await client.post(ciba_url, data=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Auth0 Error: {response.text}")
        auth_req_id = response.json().get("auth_req_id")

    print(f"[AEGIS-MCP] Push Sent! ID: {auth_req_id}")

    # 2. Polling Loop
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    poll_payload = {
        "grant_type": "urn:openid:params:grant-type:ciba",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_req_id": auth_req_id
    }

    for attempt in range(15): # Increased to 15 attempts (~75 seconds)
        await asyncio.sleep(5) # 5s interval to avoid 'slow_down'
        async with httpx.AsyncClient() as client:
            poll_res = await client.post(token_url, data=poll_payload)
            
            if poll_res.status_code == 200:
                auth_token = poll_res.json().get("access_token")
                print("[AEGIS-MCP] APPROVAL RECEIVED!")
                
                # PHASE 5: UNLOCK THE VAULT
                real_key = vault.get_secret("STRIPE_PROD_KEY", auth_token)
                print(f"[VAULT] Unlocked: {real_key[:8]}****")
                
                return {"status": "success", "vault_key_active": True}
            
            error = poll_res.json().get("error")
            if error == "authorization_pending":
                print(f"  ... waiting for user (attempt {attempt + 1})")
                continue
            else:
                return {"status": "failed", "error": error}

    raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Biometric verification timed out.")

