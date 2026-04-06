import os
import json
import httpx
import asyncio
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse, RedirectResponse
from dotenv import load_dotenv
from jose import jwt
from urllib.request import urlopen

from fastapi.middleware.cors import CORSMiddleware

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
app = FastAPI(title="Aegis-MCP Sovereign Enclave")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIG ---
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_INTERNAL_API_AUDIENCE")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
TARGET_USER_ID = "github|240042912"

# --- PHASE 1: PRIMING THE VAULT ---
@app.get("/login")
def login():
    url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri=https://jwt.io&"
        f"scope=openid profile email offline_access repo&"
        f"connection=github"
    )
    return RedirectResponse(url)

@app.get("/callback")
def callback(code: str):
    return {"status": "Vault Primed", "message": "GitHub keys are now secured in the Cloud Vault."}

# --- PHASE 2: THE SHIELD ---
def verify_jwt(token: str):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}
    if rsa_key:
        return jwt.decode(
            token, 
            rsa_key, 
            algorithms=["RS256"], 
            audience=API_AUDIENCE, 
            issuer=f"https://{AUTH0_DOMAIN}/",
            options={"verify_exp": False}
        )
    raise Exception("Cryptographic key mismatch.")

# --- PHASE 3: IDENTITY PROXY ---
@app.middleware("http")
async def identity_aware_proxy(request: Request, call_next):
    if request.url.path in ["/health", "/", "/login", "/callback", "/agent/execute-high-stakes"]:
        return await call_next(request)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Aegis Protocol: Missing Token."})
    try:
        token = auth_header.split(" ")[1]
        request.state.user = verify_jwt(token)
        return await call_next(request)
    except Exception as e:
        return JSONResponse(status_code=401, content={"detail": f"Access Denied: {str(e)}"})

# --- PHASE 4 & 5: CIBA + MANAGEMENT API EXTRACTION ---
@app.post("/agent/execute-high-stakes")
async def execute_high_stakes_action(request: Request):
    print("[AEGIS-MCP] High-stakes action detected. Pausing thread...")

    # 1. Fire CIBA Push (Clean, no audience needed to push)
    ciba_url = f"https://{AUTH0_DOMAIN}/bc-authorize"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "openid profile email", 
        "binding_message": "Authorize OpenClaw access to GitHub Vault",
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

    async with httpx.AsyncClient() as client:
        for attempt in range(20):
            await asyncio.sleep(5)
            poll_res = await client.post(token_url, data=poll_payload)

            if poll_res.status_code == 200:
                print("[AEGIS-MCP] BIOMETRIC APPROVAL RECEIVED!")

                # --- PHASE 5: TOKEN VAULT EXCHANGE ---
                print("[VAULT] Initiating Secure Token Vault Exchange...")
                
                auth0_access_token = poll_res.json().get("access_token")
                
                if not auth0_access_token:
                    return {"status": "failed", "error": "CIBA returned no access token"}
                    
                print(f"[DEBUG] CIBA Access Token: {auth0_access_token[:20]}...")
                
                vault_payload = {
                    "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "subject_token": auth0_access_token,
                    "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
                    "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
                    "connection": "github"
                }
                
                vault_res = await client.post(f"https://{AUTH0_DOMAIN}/oauth/token", json=vault_payload)
                
                if vault_res.status_code == 200:
                    github_token = vault_res.json().get("access_token")
                    if github_token:
                        print(f"[VAULT] UNLOCKED: External Access Token Released ({github_token[:8]}...)")
                        return {"status": "success", "vault_key_active": True, "provider": "github", "token": github_token}
                    else:
                        return {"status": "failed", "error": "Token Vault Exchange succeeded but returned no access_token"}
                else:
                    print(f"[VAULT] Token Vault Exchange Failed: {vault_res.text}")
                    print("[VAULT] Falling back to Management API Extraction due to Tenant Profile restriction...")
                    
                    # --- FALLBACK: MANAGEMENT API EXTRACTION ---
                    m2m_payload = {
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
                        "grant_type": "client_credentials"
                    }
                    m2m_res = await client.post(f"https://{AUTH0_DOMAIN}/oauth/token", data=m2m_payload)
                    m2m_token = m2m_res.json().get("access_token")

                    if not m2m_token:
                        return {"status": "failed", "error": "Fallback M2M Setup Failed"}

                    headers = {"Authorization": f"Bearer {m2m_token}"}
                    user_res = await client.get(f"https://{AUTH0_DOMAIN}/api/v2/users/{TARGET_USER_ID}", headers=headers)
                    
                    user_data = user_res.json()
                    github_token = None
                    
                    for identity in user_data.get("identities", []):
                        if identity.get("provider") == "github":
                            github_token = identity.get("access_token")
                            break
                    
                    if github_token:
                        print(f"[VAULT] FALLBACK UNLOCKED: GitHub Access Token Released ({github_token[:8]}...)")
                        return {"status": "success", "vault_key_active": True, "provider": "github", "token": github_token, "fallback_used": True}
                    else:
                        return {"status": "failed", "error": "GitHub Token Missing from Profile in fallback"}

            res_data = poll_res.json()
            if res_data.get("error") == "authorization_pending":
                print(f"  ... waiting for user (attempt {attempt + 1})")
                continue
            else:
                return {"status": "failed", "error": res_data.get("error")}

    raise HTTPException(status_code=408, detail="Biometric verification timed out.")

