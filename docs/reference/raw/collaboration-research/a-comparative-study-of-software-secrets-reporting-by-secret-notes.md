# A Comparative Study of Software Secrets Reporting by Secret Detection Tools (source notes)

> Source: https://ar5iv.labs.arxiv.org/html/2307.00714
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-08 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: nonexclusive-distrib — arxiv.org/abs/2307.00714 license link: arxiv.org/licenses/nonexclusive-distrib/1.0/. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/ar5iv-labs-arxiv-org-77d0c524/001.md.
> Work: arxiv:2307.00714
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

An empirical software-security paper (read via the ar5iv HTML rendering of its arXiv entry) by Setu Kumar Basak, Jamison Cox, Bradley Reaves and Laurie Williams of North Carolina State University. It compares nine secret-detection tools (five open-source, four proprietary) on the SecretBench benchmark. The visible text acknowledges NSF grant 2055554. The page itself shows no explicit publication date.

## Key facts

- Motivation: the paper cites GitGuardian's report that secrets sprawl accelerated in 2022 by 67% compared with 2021, exposing over 10 million secrets such as API keys and credentials.
- It cites the September 2022 Uber incident, where hard-coded admin credentials in PowerShell scripts were used by an attacker.
- Research questions: RQ1 on precision and recall of detection; RQ2 on features that help prevent secret exposure.
- Benchmark: SecretBench, 818 public GitHub repositories, 97,479 labelled candidate secrets of which 15,084 are true, 4,457 of those unique; eight categories (Private Key 5,789 true; API Key and Secret 4,529; Authentication Key and Token 3,569; Other 524 of 66,690; Generic Secret 334; Database and Server URL 162; Password 150; Username 27); 49 programming languages and 311 file types.
- Tool selection: 20 tools were found, 11 excluded, 9 kept. Criteria were accessible, scans Git repositories, active in the last two years, flags individual secrets, reports plain-text secrets.
- Tools and versions run: git-secrets 1.3.0, Gitleaks 8.2.7, Repo-supervisor 3.2.0, TruffleHog 3.18.0, Whispers 2.1.5, ggshield 1.14.3, plus GitHub Secret Scanner, SpectralOps and an anonymised vendor called Commercial X.
- Matching method: reported secrets were compared to the benchmark with Jaro-Winkler similarity (match at 0.7 or above) and Gestalt pattern matching (0.6 or above); a manual check of 100 secrets per tool found 97% correctly labelled.
- Findings on precision: GitHub Secret Scanner 75%, Gitleaks 46%, Commercial X 25%; five of nine tools scored below 7%.
- Findings on recall: Gitleaks 86% (Case 1) and 88% (Case 2); TruffleHog 31% and 52% with only 6% precision. F1: Gitleaks 60%, GitHub Secret Scanner 48%, Commercial X 32%.
- The authors conclude that no current tool combines high precision and high recall, and that tools overlap only partly, so relying on one tool is risky.
- Scan time on a 15-repository sample: Repo-supervisor 0.32 minutes, Whispers 0.91, git-secrets 6.71; ggshield was slowest at 4.8 hours.
- False-positive causes found: generic regular expressions, ineffective entropy calculation (TruffleHog entropy 4.08 versus 4.11 example) and insufficient filters.
- False-negative causes: faulty regexes, skipping file types (ggshield skips HTML), and insufficient or stale rulesets (Whispers rules last updated August 25, 2021).
- Seven feature categories F1 to F7: pre-commit hook, CI/CD integration, custom rules, secret verification, remediation steps, IaC scanning, non-source-code scanning (OCR for images and PDFs).
- Verification effect: TruffleHog precision was 6% with almost 100K alerts, but 90% with verification enabled (`--only-verified`) at 611 secrets.
- Only 66 API vendors had joined GitHub's secret scanning partner program, per the authors.
- Recommendations: choose tools by secret type, vendors should refresh rules, collaborate with API vendors on verification, and automate revoke and rotate; the authors cite research that attackers start using leaked API keys within one minute.
- Ethics: the false-positive dataset (BigQuery) is shared only with researchers and tool developers who sign a data protection agreement.
- Stated threats to validity: tool list is not exhaustive, SecretBench was curated using Gitleaks and TruffleHog (bias), only GitHub repositories, and string-matching cut-offs.

## Related

- SecretBench (arXiv 2303.06729), GitGuardian ggshield, Gitleaks, TruffleHog, GitHub secret scanning. Relevant to scanning shared agent sessions for leaked credentials before publication.
