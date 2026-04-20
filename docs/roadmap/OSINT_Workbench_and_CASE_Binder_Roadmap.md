# OSINT Investigation Workbench + CASE Binder Builder Roadmap

This roadmap combines the OSINT Investigation Workbench platform and the CASE Binder Builder into one coordinated product plan.

It is grounded in the existing scaffold direction, the later v0.4.3 workbench trajectory, and the separate binder/adjudicator pipeline work already described in project materials. fileciteturn28file0 fileciteturn28file2 fileciteturn28file1

---

## 1. Product Vision

Build an investigation platform that can:
- ingest and normalize intelligence from multiple sources
- correlate entities, observables, claims, and contradictions
- maintain canonical evidence and derived graph/timeline views
- drive analyst review workflows
- generate tribunal-grade case binders and adjudicator-ready decision packs

The Workbench side answers: **what happened, who is connected, what conflicts, and what matters**.

The CASE Binder side answers: **how to package that record into a defensible, indexed, page-accurate, tribunal-usable submission**.

---

## 2. Core Principles

### Canonical data model
- Postgres is the system of record
- MinIO stores raw and derived artifacts
- Neo4j is a derived graph view
- reasoning outputs are derived, inspectable, and reproducible

### Evidence integrity
- preserve raw source outputs
- separate raw, normalized, and derived views
- keep chain-of-transformation auditable
- never depend on graph as source of truth

### Tribunal usability
- binder output must be readable, printable, clickable, and page-stable
- every claim should be traceable to source artifacts
- decision-support inserts must remain grounded in actual record evidence

---

## 3. Product Modules

### A. OSINT Investigation Workbench
1. investigation control plane
2. target management
3. connector execution
4. normalization pipeline
5. graph projection
6. timeline reconstruction
7. contradiction detection
8. claim weighting and credibility scoring
9. analyst interface
10. reporting and exports

### B. CASE Binder Builder
1. evidence ingestion from case folders and merged PDFs
2. exhibit classification and dedupe
3. exhibit index generation
4. page resolver and exhibit-page mapping
5. contradiction extraction
6. decision packet generation
7. hearing script generation
8. adjudicator quick packet generation
9. binder assembly with TOC/bookmarks/cross-links
10. hearing pack and draft order generation

---

## 4. Unified End-to-End Flow

```text
Raw Sources / Evidence Files
        ↓
Connector Runs / Manual Imports / PDF Ingestion
        ↓
Normalization into Canonical Records
        ↓
Entities / Observables / Claims / Artifacts / Timeline Events
        ↓
Derived Views: Graph / Timeline / Contradictions / Reasoning
        ↓
Analyst Review + Claim Disposition + Entity Resolution
        ↓
Binder Planning: exhibit selection / indexing / page mapping
        ↓
Tribunal Outputs: disclosure packet / full binder / core packet / hearing pack / draft order
```

---

## 5. Roadmap by Version

## Phase 0 — Foundations

### v0.1 Scaffold
Status: concept/prototype baseline
- Docker Compose stack
- FastAPI app
- Postgres schema and CRUD
- Celery queue
- early connectors
- timeline write-back after connector runs fileciteturn28file0

### v0.2 Canonical evidence architecture
- formalize Postgres + MinIO + Neo4j separation
- define canonical schemas for investigations, targets, entities, observables, relationships, claims, contradictions, artifacts, jobs, runs
- isolate each connector behind shared contract
- treat graph as derived projection only

### v0.3 Execution hardening
- connector dispatch from API to Celery
- persistence of raw connector output into MinIO
- normalized write-back into Postgres
- artifact listing and retrieval endpoints
- graph projection jobs
- target/run detail pages

---

## Phase 1 — Investigation Platform Baseline

### v0.4.3 Analyst controls and search
Already aligned with:
- search across entities, observables, claims, artifacts
- analyst controls for claim approve/reject
- entity merge/split/reset
- watchlists and alerts
- contradiction detection and UI surfacing
- timeline endpoint and materialized timeline artifacts
- lightweight graph canvas UI fileciteturn28file2

### v0.4.4 Hardening pass
- Alembic migrations
- auth/RBAC
- richer graph explorer interactions
- saved-search execution
- stronger contradiction rules
- real entity resolution scoring fileciteturn28file2

### v0.5 / v1 Full baseline
- FastAPI + JWT auth
- Alembic-managed schema
- MinIO raw/artifact storage
- Neo4j graph projection
- React frontend
- real async job flow for manual import and selected enrichers
- graph, timeline, and report artifacts
- Dockerized developer baseline

Deliverable:
- usable analyst-facing baseline for investigation creation, target management, job runs, graph/timeline viewing, and artifact browsing

---

## Phase 2 — Analyst Interface

### v1.1 Analyst interface
- force-directed graph workspace
- node drag/pin/expand/filter
- relationship labels
- timeline panel with grouped event types and contradiction markers
- contradiction panel with score, reason, analyst disposition controls
- evidence workspace with artifact browser and metadata preview
- cleaner case shell: investigations, targets, job runner, status indicators

Deliverable:
- analysts no longer work from raw JSON; they operate from graph/timeline/contradiction/evidence views

---

## Phase 3 — Reasoning Layer

### v1.2 Reasoning engine
- semantic contradiction heuristics beyond exact mismatch
- claim weighting from confidence, corroboration, recency, and source factors
- credibility scoring for entities/sources
- argument builder for supporting/opposing claim bundles
- reasoning APIs and derived artifacts
- inspectable score components, not black-box outputs

Deliverable:
- machine-assisted but reviewable reasoning summaries for analyst decisions and binder generation

### v1.3 Decision layer
- decision summary builder
- issue mapping and finding clustering
- remedy recommendation support
- adjudicator-style decision pathways
- draft order scaffolding

This phase should build toward the type of outputs already present in the separate adjudicator decision engine work, including findings, credibility matrices, recommended remedies, and draft order text. fileciteturn28file1

---

## Phase 4 — CASE Binder Builder Baseline

### v2.0 Evidence ingestion and classification
- scan working directories and external media roots
- classify evidence into stable buckets such as chronology, maintenance, pest, fire, lockout, financial, unclassified
- detect duplicate and near-duplicate PDFs/images
- maintain master exhibit index
- support curated disclosure/adjudicator/full packet subsets

### v2.1 Exhibit page resolver
- compute exhibit-to-page mappings from actual compiled PDFs
- maintain stable page references
- detect unresolved page refs
- support partial page-accurate and final page-accurate index modes

This roadmap item is directly informed by the need for final page-number injection and the earlier partial index work. fileciteturn28file3 fileciteturn28file4

### v2.2 Binder assembly engine
- generate full binder
- generate disclosure packet
- generate adjudicator/core packet
- generate extracts: timeline, contradictions, orders requested, compensation
- bookmarks, clickable TOC, cross-links, consecutive page numbering
- front matter and tribunal-friendly decision packet inserts

### v2.3 Hearing pack engine
- hearing script
- anticipated defenses / rebuttals
- rapid-response answer sheet
- questioning map
- large-text hearing sheet linked to exhibit IDs/pages
- hearing day command binder

---

## Phase 5 — Adjudicator / Tribunal Decision Support

### v3.0 Adjudicator decision engine integration
Integrate outputs resembling:
- adjudicator findings
- credibility matrix
- issue mapping
- recommended remedies
- draft tribunal order
- decision summary JSON fileciteturn28file1

### v3.1 Tribunal packaging polish
- front page and cover sheet generation
- compensation summary injection
- requested orders formatting
- legal-fit validator
- pass/fail readiness report

### v3.2 Live hearing mode
- exhibit navigation panel
- script navigation tied to exhibits
- real-time contradiction lookup
- questioning assist
- transcript and tagging integration

---

## 6. Cross-Cutting Workstreams

### Data and schema
- canonical model evolution
- migrations and backfills
- dedupe intelligence
- provenance fields on claims and artifacts

### Connectors
- manual import
- IP/domain enrichment
- username/email/social adapters where lawful and authorized
- evidence-folder and merged-PDF ingestion adapters

### Search and review
- investigation-wide search
- saved filters
- analyst dispositions
- entity resolution review queue

### Integrity and compliance
- audit trail
- immutable raw artifact retention
- deterministic derived artifact generation
- environment separation and access control

### Performance and ops
- Celery queue partitioning
- background projection/materialization jobs
- observability
- deployment safety
- storage lifecycle controls for large evidence sets

---

## 7. Repo / Service Layout Target

```text
repo/
  api/
  worker/
  shared/
  frontend/
  infra/
  alembic/
  docs/
    roadmap/
    architecture/
    binder/
  scripts/
  binder/
    ingestion/
    classify/
    dedupe/
    page_resolver/
    assembly/
    hearing_pack/
    decision_support/
```

The binder system should live as a first-class subsystem rather than as disconnected ad hoc scripts.

---

## 8. Milestone Deliverables

### Milestone A — Investigation baseline
- create investigation
- add targets
- run connectors
- inspect graph/timeline/artifacts
- authenticate users
- persist raw and derived artifacts

### Milestone B — Analyst workstation
- graph workspace
- timeline workspace
- contradiction workspace
- evidence workspace
- analyst controls for claim/entity review

### Milestone C — Reasoning baseline
- weighted claims
- inspectable contradictions
- credibility summaries
- argument bundles
- reasoning summary endpoint

### Milestone D — Binder baseline
- evidence scan/classify/dedupe
- exhibit index
- page resolver
- full binder build
- disclosure packet build
- adjudicator packet build

### Milestone E — Hearing/decision system
- hearing day pack
- quick packet
- adjudicator decision support
- draft order generation
- readiness validator

---

## 9. Recommended Build Sequence

1. stabilize v1 baseline on clean repo structure
2. build v1.1 analyst interface
3. build v1.2 reasoning engine
4. add dedicated claim/contradiction/reasoning endpoints
5. create binder subsystem under `binder/`
6. build page resolver and exhibit index pipeline
7. build binder assembly engine
8. integrate adjudicator decision outputs
9. add live hearing mode and packaging validators

---

## 10. Success Standard

The final system should let an analyst:
- investigate a target or dispute record
- inspect entities, observables, contradictions, and timeline events
- review credibility and argument structure
- select and map supporting exhibits
- generate a tribunal-grade binder and hearing pack
- produce decision-support outputs grounded in actual record evidence

That is the combined destination for the OSINT Investigation Workbench and CASE Binder Builder.
