import requests
import time

# This represents the AI Agent (OpenClaw)
def open_claw_task():
    print("\n" + "="*40)
    print("[OpenClaw] Goal: Pay for server hosting via Stripe.")
    print("[OpenClaw] Requesting biometric approval via Aegis-MCP...")

    url = "http://127.0.0.1:8001/agent/execute-high-stakes"

    # FRESH TOKEN (Issued April 4, 2026)
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNoYVFucDRhN21ydWhSNUNUTGpVMCJ9.eyJpc3MiOiJodHRwczovL2Rldi1vZW0yYmk0OGt6ZjhuczJyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJ2ZWhuZ3NodTRhbFZwd3NORFhqNkdlTDg3NlJyR3lvSEBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9hcGkuYWVnaXMubG9jYWwiLCJpYXQiOjE3NzUzMjIxOTUsImV4cCI6MTc3NTQwODU5NSwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoidmVobmdzaHU0YWxWcHdzTkRYajZHZUw4NzZSckd5b0gifQ.GRjUEmSxDqw2LQHk9E1zLAxa6vhR72KtlrqC16TRa9G6--yY1NFMEVH45rk03BZIjUhSZ43E8AxLT8ORPU_55r4EYpBQJ8SNajWyQ4prDG0cxsxGCL0XB74RS4Bmo-myJdqWJPxNaYwrHNknzczIDyagvGcBMnws1D3dFfKro4NaIjsIDDwYaPo5vCFmiBLpiiGqpsJl4bRiaXGpdDqHUn8HszXa1RJLlHW3UZgRvwCqQwS33NJtmXZ3WFzSTXMoAR_ZxOICWqFeLtV5afPL4f92v8wSwDOlnJk1zptzB4gPWj_8WOLNpLcK54vmbGz-q_hBzyuFzznLnGIPnXMydg"

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Long timeout to allow you time to approve on your phone
        response = requests.post(url, headers=headers, timeout=120)

        if response.status_code == 200:
            result = response.json()
            print(f"[OpenClaw] Access GRANTED. Status: {result['status']}")
            print(f"[OpenClaw] Vault Security: {'ACTIVE' if result.get('vault_key_active') else 'INACTIVE'}")
            print("[OpenClaw] Task Complete. Keys have been flushed from memory.")
            print("="*40 + "\n")
        else:
            print(f"[OpenClaw] Access DENIED: {response.text}")

    except Exception as e:
        print(f"[OpenClaw] Logic Error: {e}")

if __name__ == "__main__":
    open_claw_task()

