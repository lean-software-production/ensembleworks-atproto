# Implementing Secrets Scanning In Ci Cd (Grade A) - Claude Skill (source notes)

> Source: https://www.skillsdirectory.com/skills/yanacuti1121-implementing-secrets-scanning-in-ci-cd
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-11 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — Directory page footer: All rights reserved 2026 Skills Directory; mirrored SKILL.md frontmatter claims Apache-2.0 but no license text with notice at this URL. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/skillsdirectory-com-91421647/001.md.
> Work: https://www.skillsdirectory.com/skills/yanacuti1121-implementing-secrets-scanning-in-ci-cd
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A listing page on the Skills Directory site for a Claude skill named `implementing-secrets-scanning-in-ci-cd`, showing the skill's `SKILL.md`. The listing credits the account yanacuti1121 and links to a source file in that account's Yana-AI repository on GitHub. The skill's own frontmatter names the author as mahipal and cites an upstream repository, mukul975/Anthropic-Cybersecurity-Skills. The page is a third-party mirror; site footer states all rights reserved. Listing shows Added September 9, 2026.

## Key facts

- The skill is about wiring gitleaks and trufflehog into CI/CD pipelines to detect leaked secrets before deployment; it is domain cybersecurity, subdomain devsecops, version 1.0.
- Frontmatter declares `license: Apache-2.0`, a pinned `source_commit` for the upstream repository, and maps to NIST CSF items PR.PS-01, GV.SC-07, ID.IM-04 and PR.PS-04 and MITRE ATT&CK items T1195, T1554 and T1059.004.
- Method described: gitleaks scans git repos and directories for hardcoded secrets with regex patterns and entropy analysis; TruffleHog scans filesystems and git history and can verify secrets against live services. Together they give broader coverage and a CI gate that blocks deployments with high-severity findings.
- Prerequisites listed: Python 3.9 or later, gitleaks v8.x, trufflehog v3.x, a git repo or directory, and a CI platform (GitHub Actions, GitLab CI, Jenkins).
- Eight steps: install the tools; create a `.gitleaks.toml` for custom rules, allowlists and path exclusions; run `gitleaks dir --source .` with JSON report options; run `trufflehog filesystem` with `--json`; parse and filter findings by severity with a bundled agent script; add a pre-deployment CI gate using gitleaks `--exit-code`; set up a pre-commit hook with `gitleaks protect --staged`; triage false positives via `.gitleaksignore` and rotate confirmed leaked credentials immediately.
- Expected output: a JSON report with total findings per scanner, findings grouped by severity, per-finding file path, line number, rule ID and redacted secret, a pass/fail CI verdict by severity threshold, and execution metadata. The sample shows 3 findings (1 critical, 1 high, 1 medium) and a `FAIL` gate.
- The site's own security grade for the skill is A (100/100), scanned September 9, 2026; the listing shows 3 stars. Files in the skill: LICENSE, SKILL.md, references/api-reference.md and scripts/agent.py.
- The content is generic template-style guidance (the When to Use section is boilerplate), not original research. Relevance to session sharing: a practical pattern for scanning agent traces and repos for leaked secrets before publishing.

## Related

- gitleaks and trufflehog projects
- mukul975/Anthropic-Cybersecurity-Skills (cited upstream)
