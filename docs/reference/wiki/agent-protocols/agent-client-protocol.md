# Agent Client Protocol (ACP)

> Sources: See attributed source contributions below; publication dates unknown unless stated.; source inventory: 0xSero/pi-acp (source notes) (attributed source notes; Unknown); svkozak/pi-acp (Sergii Kozak, svkozak/pi-acp; Unknown); agentclientprotocol/agent-client-protocol (agentclientprotocol/agent-client-protocol contributors (Apache-2.0 licensed); Unknown); Introduction - Agent Client Protocol (Agent Client Protocol contributors, agentclientprotocol/agent-client-protocol (Apache-2.0); Unknown)
> Raw: [0xsero-pi-acp-notes](../../raw/pi/0xsero-pi-acp-notes.md); [svkozak-pi-acp](../../raw/pi/svkozak-pi-acp.md); [agentclientprotocol-agent-client-protocol](../../raw/agent-protocols/agentclientprotocol-agent-client-protocol.md); [introduction-agent-client-protocol](../../raw/agent-protocols/introduction-agent-client-protocol.md)
> Updated: 2026-10-24

## Overview

ACP connects agent clients such as editors to coding agents. Pi adapters translate that client protocol to native pi APIs, with compatibility and persistence boundaries that must be checked per adapter.

## RPC adapter by 0xSero

The 0xSero/pi-acp adapter spawns pi in RPC mode, translates client requests and streams output and tool events back over newline-delimited JSON on standard input/output. It maintains a session map across restarts and forwards pi slash commands. This establishes an adapter architecture, not a guarantee of full native-history portability. The README mentions MIT without a detected license file, so its exported source is notes.

## svkozak adapter and client compatibility

The svkozak adapter also bridges ACP stdio requests to a pi RPC process. It maps tool execution to client tool updates and resolves relative locations against the session working directory; edit locations and structured diffs are best-effort. Loading uses a persistent mapping to native pi session files. Context usage depends on pi returning the necessary statistics, and the README warns that client compatibility varies. This is a separate implementation from 0xSero’s adapter, not evidence of identical feature support.

## Schema artifacts versus runtime implementations

The ACP repository defines editor-to-coding-agent communication. Its root Rust crate exposes wire-message and envelope types; implementers are directed to a higher-level runtime crate for client/agent runtime APIs. Versioned JSON Schemas are release artifacts for generators. Artifact crate/schema versions should not be assumed to identify a client’s complete supported capability set; adapter and client behavior still require compatibility checks.

## Local and remote scope in the introduction

The ACP introduction defines local subprocess communication over JSON-RPC stdio and describes remote HTTP/WebSocket scenarios as work in progress. It reuses MCP JSON representations where possible while adding coding-oriented types such as diffs. Markdown is the default user-readable text format. Remote suitability is an intended scope, not a claim that every client and agent adapter implements a finished remote deployment contract.

## Related compiled concepts

- [Agent Protocol Boundaries](protocol-boundaries.md)
- [bb Pi Provider Integration](../bb/bb-pi-provider-integration.md)
