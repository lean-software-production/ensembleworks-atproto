# Guidelines 02/2025 on processing of personal data through blockchain technologies (source notes)

> Source: https://www.edpb.europa.eu/documents/guideline/guidelines-022025-on-processing-of-personal-data-through-blockchain_en
> Resolved: https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf
> Collected: 2026-10-23
> Published: 2026-07-07
> Representation: Source notes written by fetcher-10 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — no license statement on the document page. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/edpb-europa-eu-f768f345/001.md.
> Work: https://www.edpb.europa.eu/documents/guideline/guidelines-022025-on-processing-of-personal-data-through-blockchain_en
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

European Data Protection Board Guidelines 02/2025 on processing of personal data through blockchain technologies. The text digested here is Version 2.0, adopted on 07 July 2026 after public consultation; the version history lists version 1.1 of 08 April 2025 as the pre-consultation adoption. The document page itself is thin (it links the PDF, a track-changes DOCX, a consultation report and a 2025 summary), so these notes come from the v2 PDF. Relevance to ATProto: public repositories and logs share the append-only, replicated, hard-to-delete properties the guidelines analyse, which bears on putting agent sessions into a public network.

## Key facts

- The guidelines define the blockchain properties they address as distributed, disintermediated, consistent and tamperproof, and transparent, and note that implementations can modify or restrict these.
- They state that blockchain is only a technology and not by itself a processing of personal data, but it affects GDPR compliance, so a prior evaluation is needed and should feed into the DPIA.
- Evaluation questions: whether on-chain data contains personal data, why a blockchain is necessary, what type of blockchain, and which technical and organisational measures.
- Transaction identifiers such as public keys can be personal data when they can identify a natural person by means reasonably likely to be used. Replacement values for hidden identifiers may still be personal data. IP addresses seen when interacting with a chain can also be personal data.
- On-chain data is not only transaction payload; other structures (wallet addresses, event logs, receipts, state transitions, smart contract storage) can contain personal data.
- Storing personal data as plain text on-chain is strongly discouraged. Preferred approaches: keep personal data off-chain and put only a proof of existence on-chain (pointer, cryptographic commitment, or keyed hash).
- Encryption: encrypted personal data remains personal data; deleting the key may make data unintelligible only until the algorithm is broken or the key leaks, and long retention erodes even strong encryption.
- Hashing: a salted or keyed hash is still personal data; unsalted or unkeyed hashes are generally insufficient on a public blockchain; the off-chain store creates another processing component with its own risks.
- Commitments: with a perfectly hiding scheme, deleting the original data and witness leaves a useless on-chain commitment.
- The board says technical impossibility cannot justify GDPR non-compliance, citing its ChatGPT Taskforce report.
- Article 25(2) GDPR is cited: by default personal data should not be accessible to an indefinite number of people without the subject's intervention. Public chains should be used only if public access is necessary for a purpose.
- Roles: governance decides controller and processor allocation. Permissioned blockchains give clearer responsibility and organisations should favour them. Public permissionless nodes may be controllers or joint controllers when they decisively influence purposes and essential means; a consortium or legal entity among nodes is strongly encouraged.
- Principles discussed: fairness, transparency, purpose limitation, data minimisation (append-only growth is in tension), accuracy, storage limitation, integrity and confidentiality.
- Retention: the lifetime of the blockchain is not an appropriate default retention period; data should be deleted or anonymised at the end of the processing. Where retention is not the chain lifetime, personal data should not be written to the chain unless identification is effectively prevented.
- International transfers: nodes outside the EU raise Chapter V GDPR issues; the example given is incorporating standard contractual clauses into contracts signed before a node is accepted.
- Security: assess misuse safeguards such as 51% attacks, protect keys, plan for algorithm failure with an emergency update plan, and document governance of protocol changes. Quantum-computing risk to encryption is mentioned as part of obsolescence assessment.
- If an appropriate security level cannot be reached with a blockchain, controllers should not use it for personal data.
- DPIA content for blockchain processing: systematic description, necessity and proportionality, risk assessment of the whole processing, and specific mitigation measures. A DPIA may need to be ongoing for permissionless chains, uncontrolled infrastructure or international transfers.
- Data subject rights: access and portability can be compatible with chains; erasure, objection and rectification must be handled by design, typically by making on-chain data anonymous after erasing off-chain data. Rectification may be met by a later cancelling transaction. Smart contracts may constitute automated decision-making under Article 22.
- Annex A lists 16 numbered recommendations, including: document the architecture rationale; store additional personal data off-chain; inform data subjects; minimise; assure trust in software and nodes; handle vulnerabilities; govern change; be careful with consent; apply data protection by design and default; set retention; evaluate security; protect confidentiality; and fulfil data subject rights.
- Annex B is a glossary (consensus, fork, ledger, node, proof of work and others).
- The text cites MiCA and the AML Regulation retention duties of at least five years after the end of a business relationship, with AMLR applicable from 10 July 2027.

## Related

- EDPB Guidelines 4/2019 on data protection by design and by default
- EDPB guidelines on controller and processor concepts, and on legitimate interest (1/2024)
- AEPD technical note on blockchain and the right to erasure
