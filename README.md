# Aegis-MCP: Headless Asynchronous Token Vault for Sovereign AI Agents

**Winner of the "Authorized to Act" 2026 Hackathon Paradigm**

Aegis-MCP is a secure headless adapter for sovereign AI agents (like OpenClaw) that implements a "Zero-Trust" perimeter for local AI execution. It solves the catastrophic **OpenClaw CVE-2026-25253** (Remote Code Execution) and bridges the gap between local agent autonomy and enterprise-grade Auth0 security.

## 🚀 The Core Anomaly: Headless Asynchronous Auth
Traditional AI agents break when forced into browser-based OAuth redirects. Aegis-MCP utilizes **Auth0 CIBA (Client Initiated Backchannel Authentication)** to trigger out-of-band biometric approval directly on the user's mobile device. This allows the agent to maintain its execution thread while ensuring explicit human-in-the-loop consent.

## 🛡️ Features & Security Neutralization
- **OpenClaw RCE Mitigation:** Reconfigures the OpenClaw daemon to a `trusted-proxy` mode, stripping unauthenticated WebSocket bindings and enforcing TLS termination.
- **Resilient Token Vault Integration:** Implements the **Auth0 Token Vault (RFC 8693)** for secure credential brokering. 
- **Smart Fallback Architecture:** Features a "Try-Vault, Fallback-Management" logic. If the Auth0 tenant profile is restricted, the system automatically uses the Auth0 Management API to extract JIT (Just-In-Time) credentials after biometric proof is received.
- **Identity-Aware Proxy:** A hardened middleware that intercepts agent tool calls and validates identity contexts before releasing sensitive API keys.

## 🏗️ Technical Stack
- **Backend:** Python (FastAPI, Uvicorn, Httpx)
- **Frontend:** React (Vite, TypeScript, Tailwind CSS, Shadcn/UI)
- **Identity:** Auth0 CIBA, Token Vault, Management API
- **Agent:** OpenClaw / MCP (Model Context Protocol)

## 🛠️ Setup & Demo
1. **Prime the Vault:** Access `/login` to link your GitHub/Stripe accounts to the Auth0 Cloud Vault.
2. **Launch Console:** Start the React frontend and type `simulate`.
3. **Approve:** Receive the Auth0 Guardian push notification on your mobile.
4. **Unlock:** Watch the agent retrieve the ephemeral key from the Vault and complete the high-stakes action.

---
*Developed for the Auth0 "Authorized to Act" Hackathon 2026.*
