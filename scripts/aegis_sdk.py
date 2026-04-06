import httpx
import functools

AEGIS_MIDDLEWARE_URL = "http://127.0.0.1:8001/agent/execute-high-stakes"

def with_async_authorization(action_name="high-stakes action"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n========================================")
            print(f"[OpenClaw] Intent: {action_name}")
            print(f"[OpenClaw] STATUS: HALTED. Insufficient Permissions.")
            print(f"[Aegis] Requesting Out-of-Band Biometric Approval...")
            
            try:
                # Ping the Aegis-MCP FastAPI Server (which triggers the phone push)
                # Timeout is long (120s) to give you time to tap "Approve" on your phone
                response = httpx.post(AEGIS_MIDDLEWARE_URL, timeout=120.0)
                result = response.json()
                
                if result.get("status") == "success":
                    print(f"[Aegis] BIOMETRIC SIGNATURE VERIFIED.")
                    print(f"[Aegis] JIT Credential Brokering Active. Key injected into memory.")
                    
                    # Inject the vault token into the function's arguments
                    kwargs['vault_token'] = result.get("token")
                    
                    # Resume the AI Agent's execution
                    return func(*args, **kwargs)
                else:
                    print(f"[Aegis] ACCESS DENIED: {result.get('error')}")
                    print(f"========================================\n")
                    return None
            except Exception as e:
                print(f"[Aegis] Fatal Enclave Error: {e}")
                return None
        return wrapper
    return decorator

