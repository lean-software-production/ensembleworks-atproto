# On Automated and Explainable Provenance of AI-Generated Code (source notes)

> Source: https://arxiv.org/abs/2608.02329
> Resolved: https://arxiv.org/html/2608.02329v1
> Collected: 2026-10-23
> Published: 2026-08-03
> Representation: Source notes written by fetcher-10 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: CC-BY-NC-ND-4.0 — arXiv abs page links creativecommons.org/licenses/by-nc-nd/4.0/. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/arxiv-org-1256fd2c/001.md.
> Work: https://arxiv.org/abs/2608.02329
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A short research-vision paper by Alejandro Velasco, Nathan Wintersgill, Trevor Stalnaker, Oscar Chaparro and Denys Poshyvanyk (William & Mary). It argues for explainable provenance of AI-generated code and is tied to a US National Science Foundation grant. Notes are drawn from the arXiv HTML rendering. The paper is under a no-derivatives, non-commercial license, so only notes are published.

## Key facts

- Problem statement: the origin of AI-generated code is opaque to developers, to the organizations that deploy it and to compliance staff.
- Existing mitigations (filters, detectors such as CopyrightCatcher) flag problems after generation without explaining why the model produced them.
- Attribution by link, where assistants cite web sources, is reported to give largely irrelevant references.
- Cited risks: reproduction of copyrighted fragments, exposure of memorized sensitive data, and insecure or low-quality code at scale. The lawsuit Doe v. GitHub and SBOM mandates (US Executive Order on Cybersecurity, EU Cyber Resilience Act) are cited as drivers.
- Stakeholders: model developers, model users, and compliance practitioners (including legal and OSPO staff).
- Practitioner evidence from the authors' earlier work: a survey of 574 developers found 89.7 percent regularly use CodeGenAI tools while 70.1 percent lack processes to document that use. A further survey covered 138 practitioners across five stakeholder groups.
- Developers verify origins by manual searches on GitHub and Stack Overflow, and existing compliance tools such as Black Duck and FOSSology do not cover AI-generated artifacts.
- Four traceability dimensions: prompt-to-output, instance-to-output, factor-to-output, and model component-to-output.
- Proposed techniques: propensity scoring from token log-probabilities; Local Explanation Attribution (LEA) using feature attribution such as SHAP; a retrieval pipeline mixing clone detection, neural similarity and membership inference; Global Explanation Attribution (GEA) using causal graphs and average treatment effects; and, for open-weight models only, modularization, sparse autoencoders and activation patching.
- Planned empirical study: online survey plus follow-up interviews of 40–60 minutes, run iteratively over two years, analysed with open coding and card sorting.
- Open challenges listed: provenance granularity, inaccessible training data, causal confounders, evaluation without ground truth, and bridging technical evidence with legal reasoning.
- Funding: NSF award IIS-2533367. The work is a vision and research agenda, not an evaluated system.

## Related

- Relevance to session sharing: provenance of AI-written code links to recording prompts and sessions alongside code.
- Doe v. GitHub; SBOM regimes; the authors' earlier surveys on CodeGenAI documentation and license compliance.
