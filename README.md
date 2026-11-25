# Aryan Arora

**Forward Deployed Engineer | Systems, Applied AI & Security Engineering**  
Uttarakhand, India · [LinkedIn](https://linkedin.com/in/aryanaroracs) · [GitHub](https://github.com/FROSTY-MUG) · [Email](mailto:aryanarora26110@gmail.com)

---

I build end-to-end software systems that bridge ambiguous real-world requirements with high-performance, deterministic engineering. My work spans offline-first cryptographic hardware vaults, zero-copy C++ genomic defense engines, deterministic LLM evaluation harnesses, and full-stack multi-agent workflow systems. I focus on shipping verifiable, well-tested, and production-disciplined solutions across security, systems, and applied AI.

---

## Current Focus

- **Cryptographic Storage Hardening:** Advancing `Ghost-Tag` from `v2.0.6` stable release through `v2.1.0` staging, implementing Cauchy Reed-Solomon $(N, K)$ erasure coding over $\mathrm{GF}(2^8)$ and desktop PC/SC + PN532 hardware integration.
- **Applied AI Safety & Guardrails:** Maintaining `CareSentry-AI`, refining attention-probing z-score thresholds, blockwise $O(S \cdot K)$ memory bounding, and reverse-omission detection across open-weight clinical models.
- **High-Throughput Systems:** Optimizing `Genome_Firewall` v2.0 C++14 memory-mapped FASTA ingestion pipelines and mutation-tolerant algorithmic indexing.
- **Domain-Specific Compilers:** Developing `JOCKY`, a consent-bound DFIR compiler and runtime platform in Rust and C++ for authorized incident response (SIH26148).

---

## Flagship Engineering Work

### Ghost-Tag

**Offline-first encrypted NFC data vault across Android, web, and desktop hardware.**

[Repository](https://github.com/FROSTY-MUG/Ghost-Tag) · [Live Web Client](https://frosty-mug.github.io/Ghost-Tag/) · [Security Policy](https://github.com/FROSTY-MUG/Ghost-Tag/blob/main/SECURITY.md) · [Project Status](https://github.com/FROSTY-MUG/Ghost-Tag/blob/main/PROJECT-STATUS.md)

**Problem:**  
Physical NFC tags are convenient but insecure by default. Anyone with an NFC-enabled smartphone can read unprotected user data, and lost or cloned tags expose sensitive credentials and recovery records.

**What I built:**  
Ghost-Tag encrypts user data entirely client-side and writes authenticated AES-256-GCM ciphertext envelopes to physical NTAG213, NTAG215, and NTAG216 tags. It supports single-tag vaults, multi-tag bulk file vaults with erasure coding, BIP-39 recovery phrases, cross-platform Android and web interfaces, a desktop PC/SC and PN532 hardware bridge, and opt-in zero-knowledge cloud sync.

**Engineering highlights:**
- **Two-Tier Key Hierarchy:** Derives an ephemeral KEK from a user passphrase via Argon2id; generates unique 256-bit CSPRNG DEKs per vault stored exclusively in AES-256-GCM wrapped form. KEKs and plaintexts are zeroized and never persisted.
- **Tamper-Evident Envelopes:** Additional Authenticated Data (AAD) binds envelope headers to prevent cross-tag swapping, purpose alteration, and length-extension attacks. Writes require independent byte-for-byte read-back verification.
- **Fault-Tolerant Multi-Tag Sharding:** Implemented Cauchy Reed-Solomon $(N, K)$ erasure coding over $\mathrm{GF}(2^8)$ to distribute file fragments across tag clusters, allowing full recovery from damaged tags.
- **Verification & CI/CD:** Maintained 347 Jest unit tests across 26 suites, 22 PN532 serial communication tests, CodeQL security scanning, TruffleHog secret leak prevention, and automated GitHub Pages releases.
- **Status & Boundaries:** Latest published release is `v2.0.6`; `v2.1.0` is active unreleased staging software. Protects ciphertext confidentiality against RF interception and tag tampering; does not claim forensic silicon erasure or root-compromised host defense.

**Stack:**  
`TypeScript` · `React Native` · `Kotlin` · `C++17/NDK` · `Vite` · `WebCrypto` · `Supabase` · `PostgreSQL/RLS` · `NFC / PC/SC` · `Jest` · `CodeQL`

---

### Genome Firewall (v2.0)

**High-throughput C++ antimicrobial-resistance screening and decision-support engine.**

[Repository](https://github.com/FROSTY-MUG/Genome_Firewall) · [Architecture Spec](https://github.com/FROSTY-MUG/Genome_Firewall/blob/main/docs/ARCHITECTURE.md) · [Web Console](https://github.com/FROSTY-MUG/Genome_Firewall/tree/main/web) · [API Server](https://github.com/FROSTY-MUG/Genome_Firewall/blob/main/api/server.js)

**Problem:**  
Identifying antimicrobial resistance (AMR) superbugs from raw bacterial genomes requires scanning multi-gigabyte files against massive marker catalogs with mutation tolerance under strict compute budgets.

**What I built:**  
As Project Lead and Core Architect, I engineered a pure C/C++14 systems pipeline that ingests raw FASTA genomes without external runtime dependencies, cross-references k-mers against indexed AMR catalogs, and generates tiered per-drug-class resistance predictions using an embedded logistic regression engine.

**Engineering highlights:**
- **Zero-Copy Memory-Mapped Parsing:** Built `FastaMmapParser` leveraging OS virtual memory pages (`CreateFileMapping` / `mmap`) with 64 KB chunking and overlap buffers to prevent missed markers across block boundaries.
- **Algorithmic Data Structures:** Designed a custom 4-ary genomic prefix trie (40-byte node footprint) paired with a custom 8 KB arena block allocator, indexing 4,500,462 trie nodes from the 455-marker CARD catalog.
- **Multi-Tier Fast Filtering:** Integrated a 1 MB Bloom filter with 3 hash functions for $O(1)$ fast rejection of negative sequences, alongside Hamming distance $\le 1$ mutation-tolerant searching.
- **Lock-Free Concurrency:** Implemented multithreaded sliding-window 21-mer scoring using native OS threads, immutable trie reads, and atomic counters.
- **Benchmarked Outcomes:** On an AMD Ryzen 5 hexa-core system (MinGW GCC 6.3 `-O3`), v2.0 reduced trie arena memory by 78.3% (404.8 MB to 88.0 MB), reduced inference scan time by 12x (263.27 ms to 21.99 ms), and cut total wall-clock time by 3.4x over the project's v1.0 baseline.
- **Disclaimer:** Defensive decision support only; outputs must be confirmed by standard laboratory antimicrobial susceptibility testing.

**Stack:**  
`C/C++14` · `POSIX mmap / Windows File Mapping` · `Native Threads` · `Atomics` · `Custom Allocators` · `Logistic Regression` · `Node.js` · `HTML5/Vanilla JS`

---

### CareSentry-AI

**Deterministic safety harness for open-weight medical LLMs: attention probing, clinical invariant checks, and inference-time guardrails.**

[Repository](https://github.com/FROSTY-MUG/CareSentry) · [Authors & Roles](https://github.com/FROSTY-MUG/CareSentry/blob/main/AUTHORS.md) · [Benchmark Evidence](https://github.com/FROSTY-MUG/CareSentry/blob/main/benchmark_results.json) · [Agent Skills](https://github.com/FROSTY-MUG/CareSentry/tree/main/.agents/skills)

**Problem:**  
Long clinical contexts dilute an LLM's attention to critical constraints buried in patient records, increasing the risk of missed drug allergies, adverse cross-reactivity, and unsupported treatment recommendations.

**What I co-built:**  
Co-developed a tri-layer safety harness that directly probes transformer multi-head attention weights, verifies clinical safety invariants against standardized ontologies, and enforces inference-time guardrails against prompt injection and hallucinated claims.

**Engineering highlights:**
- **Attention Probing & Statistical Scoring:** Designed PyTorch forward hooks to extract attention weights across final decision layers. Built a blockwise memory-bounded estimator operating in $O(S \cdot K)$ memory rather than $O(S^2)$ for contexts up to 24,000 tokens, coupled with depth-stratified z-score controls and bootstrap 95% confidence intervals.
- **Clinical Invariant Engine:** Implemented automated rules for cross-reactivity, renal dosing (Cockcroft-Gault CrCl & CKD-EPI 2021 eGFR), Beers Criteria, drug-drug interactions, and reverse-omission detection across 180+ drug aliases normalized via RxNorm Lite and WHO-ATC.
- **Inference Defense & Auditability:** Built prompt-injection scanners, invariant-guided constrained decoding via prefix tries, sentence-level evidence grounding, and a SHA-256 chained tamper-evident audit log with 2.47 ms CPU latency.
- **Developer Interfaces:** Delivered a Gradio clinician UI, OpenAI-compatible safety proxy gateway, Model Context Protocol (MCP) server, and three Agent Skills specifications.
- **Quality Assurance:** Backed by 130 tests across all tracks (100% passing). Tested strictly against synthetic clinical datasets; designed for local, air-gapped execution requiring human clinical oversight.

**Stack:**  
`Python 3.10+` · `PyTorch` · `Hugging Face Transformers` · `Gradio` · `MCP` · `RxNorm Lite / WHO-ATC` · `pytest` · `SHA-256`

---

## Selected Projects

| Project | Problem & Solution | Technical Stack | Verifiable Evidence |
|---|---|---|---|
| **[JOCKY](https://github.com/FROSTY-MUG/jocky-)** | Consent-bound DFIR platform and domain-specific compiler for authorized incident response on degraded hosts (SIH26148). Built lexer, AST, recursive-descent parser, and Windows C++ agent loader. | `Rust`, `C++17`, `LLVM`, `Logos`, `Shell` | [CITATION.cff](https://github.com/FROSTY-MUG/jocky-/blob/main/CITATION.cff) · [Compiler Source](https://github.com/FROSTY-MUG/jocky-/tree/main/compiler) |
| **[VC Brain](https://github.com/FROSTY-MUG/vc_brain)** | Full-stack venture deal-flow platform using LangGraph stateful multi-agent pipelines to score pitch decks, ingest PDFs, and draft investment memos. | `Next.js 16`, `FastAPI`, `LangGraph`, `Supabase`, `PyMuPDF` | [Package Manifest](https://github.com/FROSTY-MUG/vc_brain/blob/main/package.json) · [API Endpoints](https://github.com/FROSTY-MUG/vc_brain/blob/main/backend/main.py) |
| **[FP&A Studio](https://github.com/FROSTY-MUG/FPA)** | Real-time financial analysis dashboard combining Groq ultra-low-latency LPU inference, Pinecone vector embeddings, and multi-model AI forecasting. | `TypeScript`, `Next.js`, `Pinecone`, `Groq`, `Google GenAI` | [Project Metadata](https://github.com/FROSTY-MUG/FPA/blob/main/metadata.json) · [Dependencies](https://github.com/FROSTY-MUG/FPA/blob/main/package.json) |
| **[DSCPP-PBL](https://github.com/FROSTY-MUG/DSCPP-PBL)** | Academic 2D RPG engine integrating classical data structures and algorithms (SegFault Studios coursework project fork). | `JavaScript`, `Phaser 4`, `C++17`, `Vite` | [Upstream Coursework Repo](https://github.com/FROSTY-MUG/DSCPP-PBL) |

---

## Technical Capabilities

Technologies derived exclusively from verified repository usage across production and active staging code:

| Domain | Verified Technologies & Tools |
|---|---|
| **Languages** | TypeScript, JavaScript, Python, C++ (C++14/C++17), Rust, Kotlin, Swift, SQL / PLpgSQL |
| **Systems & Architecture** | Memory-mapped I/O (`mmap` / Win32), Native Multithreading, Lock-free Atomics, Arena Memory Allocators, Prefix Tries, Bloom Filters |
| **Applied AI & ML** | PyTorch, Hugging Face Transformers, LangGraph, LangChain, Attention Probing, Prompt-Injection Defense, Constrained Logit Decoding, Logistic Regression, Pinecone Vector DB |
| **Security & Cryptography** | AES-256-GCM, Argon2id, Cauchy Reed-Solomon Erasure Coding, BIP-39, SHA-256 Chained Audits, CodeQL, TruffleHog Secret Scanning, Row Level Security (RLS) |
| **Full-Stack & APIs** | Next.js (15/16), React (18/19), FastAPI, Node.js, Vite, Tailwind CSS, REST, WebSocket / NDJSON Streaming, Model Context Protocol (MCP) |
| **Hardware & Edge** | NFC (NTAG213/215/216), PC/SC Smart Card API, PN532 Serial Interfaces, React Native Android/iOS |
| **DevOps & Quality** | GitHub Actions CI/CD, GitHub Pages, Supabase / PostgreSQL, Jest (347 tests), pytest (130 tests), Dependabot |

---

## GitHub Activity

Contribution activity, language distribution, and repository health are refreshed automatically through GitHub Actions.

<!-- BEGIN:DYNAMIC_METRICS -->
| Metric | Verified Value | Source |
|---|---|---|
| **Public Repositories** | `9` | GitHub API |
| **Total Stargazers** | `5` | Verified Public Stars |
| **Automation Pipeline** | GitHub Actions | Daily refresh + push event |
| **Data Timestamp** | `2026-11-25T15:18:20.705044Z` | Automated Bot Sync |

#### Recent Repository Updates
- **[Ghost-Tag](https://github.com/FROSTY-MUG/Ghost-Tag)** (`2026-11-25`): Zero-knowledge, offline-first encrypted vaults for NFC tags — AES-256-GCM, Argon2id, Reed-
- **[FROSTY-MUG](https://github.com/FROSTY-MUG/FROSTY-MUG)** (`2026-11-25`): Active development
- **[Genome_Firewall](https://github.com/FROSTY-MUG/Genome_Firewall)** (`2026-11-22`): Active development
- **[jocky-](https://github.com/FROSTY-MUG/jocky-)** (`2026-10-17`): Active development
<!-- END:DYNAMIC_METRICS -->

### Language Distribution

<!-- BEGIN:DYNAMIC_LANGUAGES -->
| Language | Percentage | Verified Repositories |
|---|---|---|
| `TypeScript` | 37.97% `███████` | Ghost-Tag, Genome_Firewall, CareSentry, jocky-, vc_brain |
| `Python` | 22.08% `████` | Ghost-Tag, Genome_Firewall, CareSentry, jocky-, vc_brain |
| `JavaScript` | 13.55% `██` | Ghost-Tag, Genome_Firewall, CareSentry, jocky-, vc_brain |
| `C++` | 9.11% `█` | Ghost-Tag, Genome_Firewall, CareSentry, jocky-, vc_brain |
| `Rust` | 6.85% `█` | Ghost-Tag, Genome_Firewall, CareSentry, jocky-, vc_brain |
| `HTML` | 2.33% `` | Ghost-Tag, Genome_Firewall, CareSentry, jocky-, vc_brain |
<!-- END:DYNAMIC_LANGUAGES -->

---

## Open Source & Community

- **Maintainer & Lead:** Maintainer of `Ghost-Tag` (offline NFC vaults) and `jocky-` (incident response compiler).
- **Project Lead & Core Architect:** Architect of `Genome_Firewall` v2.0 (multithreaded biosecurity screening) and core author of `CareSentry-AI` (medical LLM safety harness).
- **Standards & Specifications:** Published 3 Agent Skills specifications adhering to the [Agent Skills Open Standard](https://agentskills.io) in the `CareSentry` ecosystem.

---

## Verified Engineering Experience & Competitions

- **IIT Roorkee FinCortex:** **1st Place Champion** — Engineered and deployed a multi-model real-time financial intelligence dashboard with consensus verification under a 72-hour constraint (200+ competing engineering teams).
- **IEEE Logixcape:** **1st Place Champion** — Ranked 1st across 3 rounds of advanced algorithmic problem-solving and systems logic puzzles (300+ participants).
- **Kindle Junior 4.0 (IEEE - GEU):** **1st Place Champion** — Designed and delivered an AI assessment and career recommendation workflow.
- **DigiTech Titans:** **1st Place Champion** — Solved 8 intensive full-stack and systems engineering challenges in 84 minutes.
- **Academic Foundation:** B.Tech in Computer Science & Engineering (Honours in AI & Machine Learning), Graphic Era University, Dehradun.

---

## Contact

Open to **Forward Deployed Engineer (FDE)**, **Solutions Engineer**, **Customer Engineer**, and **Applied AI / Systems Engineering** roles.

- **Email:** [aryanarora26110@gmail.com](mailto:aryanarora26110@gmail.com)
- **LinkedIn:** [linkedin.com/in/aryanaroracs](https://linkedin.com/in/aryanaroracs)
- **GitHub:** [github.com/FROSTY-MUG](https://github.com/FROSTY-MUG)
- **Portfolio:** [frosty-mug.github.io](https://frosty-mug.github.io)

---

<p align="center">
  <sub>Last refreshed automatically from public GitHub activity via GitHub Actions on P26-11-25<!-- END:LAST_UPDATED -->.</sub>
</p>
