# Secret and Context Leakage in Shared Sessions

> Sources: See attributed source contributions below; publication dates unknown unless stated.; source inventory: A Comparative Study of Software Secrets Reporting by Secret Detection Tools (source notes) (attributed source notes; Unknown); OWASP Top 10 for LLM Applications 2026 (source notes) (attributed source notes; Unknown); The lethal trifecta for AI agents: private data, untrusted content, and external communication (source notes) (attributed source notes; 2025-06-16); Guidelines 02/2025 on processing of personal data through blockchain technologies (source notes) (attributed source notes; 2026-07-07); Implementing Secrets Scanning In Ci Cd (Grade A) - Claude Skill (source notes) (attributed source notes; Unknown)
> Raw: [a-comparative-study-of-software-secrets-reporting-by-secret-notes](../../raw/collaboration-research/a-comparative-study-of-software-secrets-reporting-by-secret-notes.md); [owasp-top-10-for-llm-applications-2026-notes](../../raw/security-privacy/owasp-top-10-for-llm-applications-2026-notes.md); [2025-06-16-the-lethal-trifecta-for-ai-agents-private-data-untrusted-notes](../../raw/security-privacy/2025-06-16-the-lethal-trifecta-for-ai-agents-private-data-untrusted-notes.md); [2026-07-07-guidelines-02-2025-on-processing-of-personal-data-through-notes](../../raw/security-privacy/2026-07-07-guidelines-02-2025-on-processing-of-personal-data-through-notes.md); [implementing-secrets-scanning-in-ci-cd-grade-a-claude-skill-notes](../../raw/security-privacy/implementing-secrets-scanning-in-ci-cd-grade-a-claude-skill-notes.md)
> Updated: 2026-10-24

## Overview

Shared sessions can expose credentials, private files and tool output. Secret scanning is useful evidence, but disclosure review must also consider sensitive context that is not recognizable as a credential.

## Secret scanner evidence and limits

Basak and colleagues compare secret-detection tools against a labeled repository benchmark and find differing precision, recall and partial overlap. Generic patterns and entropy heuristics produce false positives, while skipped file types and faulty matching miss real secrets. The result supports layered review rather than treating a clean scan from one tool as proof of safety. These repository-code experiments do not directly measure transcript sanitization or leakage of non-secret private context.

## Threat taxonomy scope

The captured OWASP release index lists prompt injection, sensitive information disclosure, excessive agency and hidden context exposure among its risk categories. It points to canonical entry files, but those detailed entries are not included in this source packet. Use this as a taxonomy pointer, not evidence that a specific mitigation or compliance checklist has been validated.

## Untrusted shared history and external communication

Simon Willison argues that private-data access, untrusted input and external communication form a dangerous combination because injected instructions can redirect private data outward. Shared session transcripts are one possible untrusted input channel. Publishing or replaying them should preserve the distinction between observed content and authorized instructions. His examples and mitigation discussion support constraining capability combinations; they do not prove that a generic prompt-injection filter reliably prevents exfiltration.

## Replication and retention analogy from EDPB guidance

The EDPB blockchain guidance discusses personal identifiers, public replication, minimization and retention. It discourages plaintext personal data on-chain and notes that encryption or hashes do not automatically remove personal-data concerns. Its subject is blockchain technology, not a ruling about ATProto. The design analogy is narrower: deleting a local record or encryption key is not proof that every previously replicated copy disappears. A session publisher should plan audience, retention and removal before publication. This source digest is not a current legal assessment of any deployment.

## Practical scanner gating pattern

The mirrored CI/CD scanning skill combines Gitleaks patterns with TruffleHog filesystem/history checks and optional live verification. It recommends custom rules, redacted findings, false-positive triage, severity gates and rotation of confirmed credentials. This is template-style implementation guidance, not an empirical accuracy evaluation. Verification can itself contact services, so a publication workflow must make that choice explicit rather than equating offline inspection with live secret testing.

## Related compiled concepts

- [ATProto Spaces (Permissioned Data)](../atproto/atproto-spaces-permissioned-data.md)
- [Message Provenance and Attribution](message-provenance-and-attribution.md)
