# The lethal trifecta for AI agents: private data, untrusted content, and external communication (source notes)

> Source: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
> Collected: 2026-10-23
> Published: 2025-06-16
> Representation: Source notes written by fetcher-09 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — No license statement found in archived HTML. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/simonwillison-net-c11eb705/001.md.
> Work: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
> Quotations: 70 characters verbatim in this file; 70 of 90 allowed for this work across the knowledge base.

## About this source

A blog post by Simon Willison on his weblog, dated 16th June 2025, coining the lethal trifecta for AI agents. It is part of his Prompt injection series (item 20 in the series list).

## Key facts

- The trifecta is three capabilities in one agent: access to private data, exposure to untrusted content, and the ability to communicate externally in a way that could exfiltrate data.
- The author argues that combining all three lets an attacker trick the agent into reading private data and sending it to the attacker.
- Core reasoning: LLMs follow instructions found in content and cannot reliably tell where an instruction came from, since everything becomes one token sequence.
- Cited incidents in the preceding weeks: Microsoft 365 Copilot, GitHub's official MCP server, GitLab's Duo Chatbot. The author lists earlier cases from April 2023 (ChatGPT) to February 2025 (ChatGPT Operator) and tags dozens under `exfiltration-attacks`.
- The author argues Model Context Protocol encourages mixing tools from different sources, so users easily assemble the trifecta; an email-reading tool is an easy untrusted-content channel; any HTTP request, image load or clickable link can serve as an exfiltration path.
- The GitHub MCP exploit is given as an example of one tool mixing all three: reading public issues, accessing private repos, creating pull requests.
- The author says guardrail products claiming to catch 95% of attacks are suspect, since in web security 95% is a failing grade, and that nobody knows how to prevent this 100% reliably.
- Mitigation papers referenced: Design Patterns for Securing LLM Agents against Prompt Injections (six patterns) and Google DeepMind CaMeL; the author says neither helps end users mixing tools, whose only safe option is avoiding the trifecta.
- The author distinguishes prompt injection (mixing trusted and untrusted content, named after SQL injection) from jailbreaking.

## Quotations

- "once an LLM agent has ingested untrusted input, it must be constrained" (quoted by Willison from the design patterns paper)

## Related

- OWASP LLM Top 10 2026, MCP, session-sharing safety (untrusted shared transcripts replayed into agents).
