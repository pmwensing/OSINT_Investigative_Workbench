# 🕵️ OSINT Investigative Workbench

> Intelligence-grade OSINT platform for evidence correlation, contradiction analysis, and tribunal-ready decision systems.

---

![Status](https://img.shields.io/badge/status-active_development-orange)
![Level](https://img.shields.io/badge/grade-analyst--level-black)
![Use Case](https://img.shields.io/badge/usecase-tribunal%20%7C%20osint%20%7C%20intelligence-critical)
![Backend](https://img.shields.io/badge/backend-FastAPI-green)
![Frontend](https://img.shields.io/badge/frontend-React-blue)
![Database](https://img.shields.io/badge/database-PostgreSQL-336791)
![Graph](https://img.shields.io/badge/graph-Neo4j-008CC1)
![Storage](https://img.shields.io/badge/storage-MinIO-red)
![Queue](https://img.shields.io/badge/queue-Celery-yellow)

---

## ⚡ What This Actually Is

Most OSINT tools **collect data**.

This system is built to **prove things**.

The OSINT Investigative Workbench transforms fragmented data into:

- **Legally coherent evidence**
- **Entity-linked intelligence**
- **Time-validated event chains**
- **Contradiction & credibility analysis**
- **Decision-ready outputs for adjudicators**

This is an **intelligence system**, not just a recon toolkit.

---

## ⚖️ Built for Real Decisions

This platform is designed for environments where outcomes matter:

- Legal proceedings
- Tribunal hearings
- Investigative reporting
- Enforcement and compliance cases

### Core Principle

> Evidence must not only exist — it must be **structured, cross-referenced, and defensible**.

---

## 🧾 Tribunal-Ready Capabilities

- 📌 Evidence → Claim → Finding mapping
- 🔗 Exhibit-page resolution and traceable citations
- ⏱️ Timeline-backed causation chains
- ⚠️ Contradiction detection across sources
- 🧠 Credibility scoring foundation
- 🧾 Pre-built decision and order drafting

---

## 🎯 What It Produces

Not dashboards.

**Outcomes.**

- Adjudicator-ready summaries
- Structured findings
- Contradiction matrices
- Recommended remedies
- Draft legal and tribunal orders

---

## 🧠 Intelligence Engine

The system operates as a layered intelligence pipeline:

### 1. Data Ingestion
Multi-source OSINT collection via pluggable connectors.

### 2. Normalization
Canonical schema ensures consistency and auditability.

### 3. Evidence Storage
- Raw artifacts
- Structured data
- Derived intelligence views

### 4. Correlation
- Timeline alignment
- Entity linking
- Cross-source merging

### 5. Analysis
- Contradiction detection
- Claim clustering
- Credibility signals

### 6. Projection
- Graph intelligence
- Timeline reconstruction
- Investigation views

### 7. Output
- Decision-ready summaries
- Tribunal-grade reports
- Intelligence exports

---

## 🧱 System Architecture

```text
            ┌────────────────────────────┐
            │     External Intelligence   │
            │  (OSINT APIs / Sources)    │
            └────────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │     Connector Layer        │
            │ (Pluggable Ingestion)      │
            └────────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │        FastAPI Core        │
            │  (Normalization + Control) │
            └────────────┬───────────────┘
                         │
     ┌───────────────────┼───────────────────┐
     ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ PostgreSQL   │  │    MinIO     │  │    Celery    │
│ (Canonical)  │  │ (Evidence)   │  │ (Execution)  │
└──────────────┘  └──────────────┘  └──────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │       Neo4j Graph          │
            │  (Derived Intelligence)    │
            └────────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │     Analyst Interface      │
            │  (Graph + Timeline + UI)   │
            └────────────────────────────┘
```

---

## 🔍 Investigation Workflow

```text
Raw Data
   ↓
Evidence
   ↓
Entities
   ↓
Relationships
   ↓
Timeline
   ↓
Contradictions
   ↓
Credibility
   ↓
Findings
   ↓
Decision Output
```

This mirrors how real investigations and adjudications are decided.

---

## 🖥️ Analyst Experience

### 🕸️ Graph Intelligence
- Interactive entity graph
- Cluster detection
- Relationship tracing
- Pathfinding between actors

### ⏱️ Timeline Engine
- Event reconstruction
- Anchor alignment
- Cross-source correlation

### 📂 Evidence Workspace
- Artifact browsing
- Exhibit linking
- Claim validation

### ⚠️ Contradiction Engine
- Conflicting claims surfaced automatically
- Analyst review and resolution workflow

### 🎯 Decision Layer
- Findings builder
- Remedy suggestions
- Draft order generation

---

## 🧭 Positioning

This system sits between:

- OSINT tools
- Case management systems
- Legal evidence preparation tools

### It bridges the gap:

> From **data → intelligence → decision**

---

## 💼 Potential Use Cases

- Digital investigations
- Tenant / landlord disputes
- Fraud analysis
- Compliance investigations
- Intelligence reporting
- Legal evidence preparation

---

## 🔐 Evidence Integrity Principles

- Immutable raw evidence storage
- Reproducible processing pipeline
- Clear chain-of-transformation
- Separation of raw vs derived intelligence

---

## ⚖️ Ethical Use

This platform is designed for:

- Lawful investigations
- Authorized intelligence gathering
- Evidence-based analysis

Not for misuse, harassment, or unlawful surveillance.

---

## 🚀 Quick Start

```bash
chmod +x bootstrap_osint_workbench_v0_1.sh
./bootstrap_osint_workbench_v0_1.sh ./osint-workbench

cd osint-workbench
cp .env.example .env
docker compose up --build
```

---

## 📦 Current Direction

This repository is evolving toward a full-stack, analyst-grade OSINT and tribunal intelligence platform with structured evidence handling, graph projection, contradiction analysis, and decision support. The project direction is consistent with the earlier scaffold and platform planning already described in the workbench materials. fileciteturn0file0

---

## 🧠 Final Note

Most tools help you **find information**.

This system is built to help you **prove what happened**.
