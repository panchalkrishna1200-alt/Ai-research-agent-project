# 🤖 AI Research & Recommendation Agent

An AI-powered tool that takes any company name as input and generates a full structured intelligence report — **completely free, no API keys required**.

---

## 🚀 Quick Start

### Step 1 — Install Ollama
Download from https://ollama.com and install it.

### Step 2 — Start Ollama & pull a model
```bash
ollama serve
ollama pull llama3.2
```

### Step 3 — Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
streamlit run app.py
```

Open your browser at: **http://localhost:8501**

---

## 📁 Project Structure

```
ai_research_agent/
│
├── app.py                  # Main Streamlit UI
├── research.py             # DuckDuckGo + Wikipedia search
├── analyzer.py             # Ollama LLM integration
├── report_generator.py     # Markdown + PDF export
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🛠️ Architecture

```
User enters company name
        │
        ▼
┌─────────────────────┐
│   Research Layer    │
│  DuckDuckGo Search  │  ← 4 targeted queries
│  Wikipedia API      │  ← Company summary
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Ollama LLM Layer   │
│  (runs locally)     │  ← 5 focused prompts
└─────────────────────┘
        │
   ┌────┼────┬────────┬──────────┐
   ▼    ▼    ▼        ▼          ▼
Overview  Biz  Challenges  AI Opps  CEO Pitch
        │
        ▼
┌─────────────────────┐
│   Report Export     │
│  Markdown / PDF     │
└─────────────────────┘
```

---

## 🤖 AI Tools Used

| Tool | Purpose |
|------|---------|
| **Ollama** | Local LLM inference (no API key, no internet) |
| **LLaMA 3.2** | Default language model |
| **DuckDuckGo Search** | Free web search (no API key) |
| **Wikipedia API** | Structured company information |

---

## 📊 Report Sections Generated

1. **Company Overview** — What they do, industry, scale, geography
2. **Key Business Information** — Offerings, news, expansion plans
3. **Potential Business Challenges** — Specific operational/sales/CX issues with reasoning
4. **AI Opportunities** — Company-specific AI recommendations mapped to real challenges
5. **Personalized CEO Pitch** — One-page pitch for the CEO

---

## ⚙️ Recommended Models

| Model | RAM Required | Quality |
|-------|-------------|---------|
| llama3.2 | 4 GB | ⭐⭐⭐⭐ Recommended |
| mistral | 4 GB | ⭐⭐⭐⭐ Good |
| gemma2 | 5 GB | ⭐⭐⭐⭐ Good |
| llama3.1 | 8 GB | ⭐⭐⭐⭐⭐ Best quality |
| phi3 | 2 GB | ⭐⭐⭐ Lightweight |

---

## ❗ Troubleshooting

**"Cannot connect to Ollama"**
→ Run `ollama serve` in a terminal first

**"Model not found"**
→ Run `ollama pull llama3.2`

**Slow responses**
→ Switch to `phi3` (smaller model) in the sidebar

**DuckDuckGo rate limit**
→ Wait 30 seconds and try again

---

## 📋 Approach & Reasoning

The system uses a **multi-source research → focused analysis** pipeline:

1. Gather raw data from web + Wikipedia (multiple search queries)
2. Feed all research into focused, role-specific prompts
3. Each section uses a different expert persona (analyst, consultant, AI architect, pitch writer)
4. The model reasons based on actual company data, not generic knowledge

This ensures recommendations are **specific** to the company, not generic industry advice.

---

*No API keys · No cloud costs · Runs entirely on your laptop*
