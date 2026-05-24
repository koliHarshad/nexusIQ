## 📌 Project Overview
NexusIQ is a full-stack, AI-powered analytics engine designed to automatically detect, correlate, and diagnose system anomalies. It simulates a massive e-commerce system crash, ingests the chaotic data across multiple streams and formats, uses custom correlation algorithms to link system anomalies and passes these clustered events to Google's Gemini 2.5 Flash to validate and format the executive incident reports.

By combining a robust Python/FastAPI backend with a dynamic React frontend, NexusIQ automates the extraction, transformation, and AI-assisted evaluation of forensic data, making it actionable for investigators and analysts.

---

## 🛠️ Tech Stack
* **Frontend:** React, Vite, Recharts (Dashboard, UI Components)
* **Backend:** Python, FastAPI, Uvicorn
* **Database/Storage:** DuckDB (Relational/Structured), ChromaDB (Vector/Unstructured)
* **AI & Analytics:** Google Gemini 2.5 Flash, LangChain, Pandas, Numpy
* **Infrastructure:** Docker, Docker Compose

---

## ⚙️ Core Features
* **Chaos Engineering Simulator:** Automatically generates realistic, time-series data points mimicking a system outage (e-commerce sales drops, server 500 errors, negative Twitter sentiment).
* **Multi-Modal Data Ingestion (ETL):** Efficiently processes structured tabular data into **DuckDB** for high-performance analytical querying, and embeds unstructured social media text into **ChromaDB** for vector search.
* **Automated AI Analyst:** Scans for anomalies (e.g., 30% revenue drops) and clusters them temporally to find the root cause of an ongoing incident.
* **Generative AI Reporter:** Synthesizes technical logs and user tweets into a cohesive, human-readable executive summary and timeline.
* **Interactive Dashboard:** Presents the findings in a clean, user-friendly React interface, complete with historical audit tracking and visual metrics.

---

## 🚀 Architecture & Data Flow
1. **Simulation (`generate_data.py`):** Mocks the data streams for a specific time window.
2. **Data Layer (`etl_pipeline.py`):** Loads data into local DuckDB and ChromaDB instances.
3. **Detection (`ai_analyst.py`):** Identifies and clusters temporal anomalies.
4. **Reporting (`reporter.py`):** Generates the final AI executive report.
5. **API (`api.py`):** Exposes REST endpoints for the frontend.
6. **Dashboard:** Consumes the API to render the visual timeline and metrics.

---
## 🖥️ Dashboard Previews
## <img width="1918" height="912" alt="Screenshot 2026-05-24 202853" src="https://github.com/user-attachments/assets/3ea718f8-5b3f-4957-ae2d-c88fecf75c6a" />
## <img width="1918" height="902" alt="Screenshot 2026-05-24 202920" src="https://github.com/user-attachments/assets/7111bfa1-6eab-468e-b16a-be4646ca0eb4" />
## <img width="1918" height="905" alt="Screenshot 2026-05-24 202938" src="https://github.com/user-attachments/assets/049b9ee0-736b-478b-9425-3f4599ada339" />

---

## 🚦 Getting Started

### Prerequisites
* Python 3.10+
* Node.js & npm
* Docker & Docker Compose
* Google Gemini API Key

### 1. Environment Setup
Create a `.env` file in the root directory and add your API key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
