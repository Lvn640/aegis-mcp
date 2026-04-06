# Aegis-MCP: Headless Asynchronous Token Vault for Sovereign AI Agents

Aegis-MCP is a secure adapter for sovereign AI agents (like OpenClaw) that implements a security perimeter for local AI execution. It addresses the OpenClaw CVE-2026-25253 (Remote Code Execution) vulnerability by bridging local agent autonomy with Auth0 security.

## Features
- **Headless Asynchronous Auth:** Uses Auth0 CIBA to trigger out-of-band biometric approval on a mobile device.
- **OpenClaw RCE Mitigation:** Configures the OpenClaw daemon to `trusted-proxy` mode, enforcing TLS termination.
- **Token Vault Integration:** Implements Auth0 Token Vault (RFC 8693) for credential brokering.
- **Fallback Architecture:** Includes a "Try-Vault, Fallback-Management" logic to ensure credential delivery via the Auth0 Management API if the vault profile is restricted.
- **Identity Proxy:** Middleware that intercepts tool calls and validates identity contexts.

## Local Development Setup

### Backend Setup
1. **Clone the Repo:** `git clone https://github.com/Lvn640/aegis-mcp.git`
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Configure Environment:** 
   - Copy `server/.env.example` to `server/.env`.
   - Fill in your Auth0 credentials and `TARGET_USER_ID`.
4. **Run the Server:** 
   ```bash
   uvicorn server.main:app --host 0.0.0.0 --port 8000
   ```

## Setup & Demo
1. **Prime the Vault:** Access `/login` to link your GitHub/Stripe accounts.
2. **Launch Console:** Start the React frontend and type `simulate`.
3. **Approve:** Receive the Auth0 Guardian push notification on your mobile.
4. **Unlock:** The agent retrieves the ephemeral key and completes the action.
