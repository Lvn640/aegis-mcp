# Aegis-MCP: Sovereign Agentic Security

## Current Status: Phase 5 Verified
The biometric handshake (CIBA + Auth0) is functional. The system is in "Lab Mode" with mocked data.

## Workstream A: Real Token Vault (Identity Team)
* **Goal**: Replace `server/vault.py` with the **Auth0 Token Vault**.
* **Task**: Use Token Exchange APIs to ensure secrets never touch the local disk.

## Workstream B: MCP Protocol Adapter (AI Team)
* **Goal**: Implement a real **Model Context Protocol (MCP)** server.
* **Task**: Build `adapter/mcp_server.py` so **OpenClaw** can use Aegis as a tool.
