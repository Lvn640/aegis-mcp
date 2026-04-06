from aegis_sdk import with_async_authorization
import time

# 1. The OpenClaw Tool (Protected by Aegis)
@with_async_authorization(action_name="Delete Production GitHub Repository")
def delete_github_repo(repo_name, vault_token=None):
    print(f"\n[OpenClaw] Resuming Execution...")
    print(f"[OpenClaw] Connecting to GitHub API with token: {vault_token[:12]}********")
    time.sleep(1)
    print(f"[OpenClaw] SUCCESS: Repository '{repo_name}' has been deleted.")
    print(f"[Aegis] Task Complete. Keys flushed from agent memory.")
    print(f"========================================\n")

# 2. The Agent's Execution Loop
if __name__ == "__main__":
    print("Agent booted. Waiting for commands...")
    time.sleep(1)
    # The agent attempts to run the tool
    delete_github_repo(repo_name="aegis-core-backend")

