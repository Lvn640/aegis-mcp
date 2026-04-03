import requests
import time

# This represents the AI Agent (OpenClaw)
def open_claw_task():
    print("\n" + "="*40)
    print("[OpenClaw] Goal: Pay for server hosting via Stripe.")
    print("[OpenClaw] Requesting biometric approval via Aegis-MCP...")
    
    url = "http://127.0.0.1:8000/agent/execute-high-stakes"
    
    # Use the same token from your last successful run
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNoYVFucDRhN21ydWhSNUNUTGpVMCJ9.eyJpc3MiOiJodHRwczovL2Rldi1vZW0yYmk0OGt6ZjhuczJyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJCM2NVRTltQUF6NWJRclhOQjVkUnpJNzRBUlo0dUgxTkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9hcGkuYWVnaXMubG9jYWwiLCJpYXQiOjE3NzUxOTYwMjEsImV4cCI6MTc3NTI4MjQyMSwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoiQjNjVUU5bUFBejViUXJYTkI1ZFJ6STc0QVJaNHVIMU4ifQ.jsJ3cIF7fjtsxbzO26ln-4ZX8a-046-WX6z-YDZfqSNabQqxXA9uxNamnYeh_XuEH_ZOyTvDMnLSUJ1mnIBBe8r3x253ABuYIf2PdHI0XrW2T6Y68qENYjo_5Og0Jl7IJqgOaO3drmAgjsbscXyGG5Z5tysz-q-ahd4HRGlxTAjnZmCLjokWS1JvtAENNroWvc-BDTPx33BFzI-Z_WmNeGQJZ4kXXRUewLGmuR-UwUXLcJKPb3jPymGcGeIQJ1_x3ZD4LDd-lglZ4QPkw8g5NZjtMln-kjFf3eRF6m2y7hoi1jVrDHwd78tWz4iFRBF-0-5-v_hW5Szeoo2FxM52dA"

    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Long timeout to allow you time to approve on your phone
        response = requests.post(url, headers=headers, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            # --- THE FIX IS HERE ---
            print(f"[OpenClaw] Access GRANTED. Status: {result['status']}")
            print(f"[OpenClaw] Vault Security: {'ACTIVE' if result.get('vault_key_active') else 'INACTIVE'}")
            print("[OpenClaw] Task Complete. Keys have been flushed from memory.")
            # -----------------------
            print("="*40 + "\n")
        else:
            print(f"[OpenClaw] Access DENIED: {response.text}")
            
    except Exception as e:
        print(f"[OpenClaw] Logic Error: {e}")

if __name__ == "__main__":
    open_claw_task()

