# Agent Protocol Boundaries

> Sources: See attributed source contributions below; publication dates unknown unless stated.; source inventory: modelcontextprotocol/modelcontextprotocol (source notes) (attributed source notes; Unknown); a2aproject/A2A (a2aproject/A2A contributors (Apache-2.0 licensed); Unknown)
> Raw: [modelcontextprotocol-modelcontextprotocol-notes](../../raw/agent-protocols/modelcontextprotocol-modelcontextprotocol-notes.md); [a2aproject-a2a](../../raw/agent-protocols/a2aproject-a2a.md)
> Updated: 2026-10-24

## Overview

Agent interoperability spans client-agent interaction, tool/context interfaces and agent-to-agent delegation. Repository descriptions establish intended boundaries, not proof that sessions or permissions transfer losslessly.

## MCP specification repository scope

The MCP repository contains specification, schema and documentation, with TypeScript and JSON Schema representations. Its README license summary and collected license-file information differ; the source packet conservatively records the mixed transition instead of exporting full text. This repository inventory is not a detailed execution or permission specification and cannot establish how a particular tool server authenticates requests.

## A2A interoperability between opaque agents

The A2A project describes communication among opaque agentic applications: agents can cooperate without exposing their internal state or implementation. This is a different boundary from an editor driving an agent through ACP. For session sharing, task exchange with a remote agent does not imply the remote agent exports its full native history or grants a collaborator steering rights.

## Related compiled concepts

- [Agent Client Protocol (ACP)](agent-client-protocol.md)
- [Agent Session and Trace Formats](../agent-sessions/agent-session-trace-formats.md)
