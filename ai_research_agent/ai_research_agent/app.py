import streamlit as st
import time
from research import search_company, get_wikipedia_summary
from analyzer import analyze_with_ollama
from report_generator import generate_pdf_report, generate_markdown_report
import os

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f, #0d6efd);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .section-card {
        background: #f8f9fa;
        color: #212529;
        border-left: 4px solid #0d6efd;
        padding: 1.2rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
    }
    .section-card.challenges { border-left-color: #fd7e14; }
    .section-card.ai-opps    { border-left-color: #6f42c1; }
    .section-card.pitch      { border-left-color: #198754; }
    .section-card.biz        { border-left-color: #0dcaf0; }
    .status-box {
        background: #1e1e2e;
        border: 1px solid #bee5fb;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .metric-card {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .stExpander { border: 1px solid #dee2e6 !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Research & Recommendation Agent</h1>
    <p style="margin:0;opacity:0.9">Generate structured intelligence reports for any company — powered by Ollama (local AI) + DuckDuckGo</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    model_name = st.selectbox(
        "Ollama Model",
        ["llama3.2", "llama3.1", "mistral", "gemma2", "phi3"],
        help="Make sure the model is pulled via: ollama pull <model>"
    )
    st.markdown("---")
    st.markdown("### 📋 How to use")
    st.markdown("""
1. Make sure **Ollama** is running  
   `ollama serve`
2. Pull a model  
   `ollama pull llama3.2`
3. Enter company name
4. Click **Generate Report**
5. Download your report
    """)
    st.markdown("---")
    st.markdown("### 🔗 Stack")
    st.markdown("""
- 🦙 **Ollama** — local LLM  
- 🔍 **DuckDuckGo** — web search  
- 📖 **Wikipedia** — company info  
- 📄 **ReportLab** — PDF export  
- 🌐 **Streamlit** — UI  
    """)
    st.markdown("---")
    st.caption("No API keys required · 100% local · Free")

# ── Main Input ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    company_name = st.text_input(
        "🏢 Company Name",
        placeholder="e.g. Adani Realty, Prestige Group, Sobha...",
        help="Enter any Indian or global company name"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 Generate Report", type="primary", use_container_width=True)

# ── Report Generation ─────────────────────────────────────────────────────────
if generate_btn and company_name.strip():
    st.markdown("---")
    progress_bar = st.progress(0)
    status_placeholder = st.empty()

    def update_status(msg, pct):
        status_placeholder.markdown(f'<div class="status-box">⏳ {msg}</div>', unsafe_allow_html=True)
        progress_bar.progress(pct)

    report_data = {}

    try:
        # Step 1 – Research
        update_status(f"Searching the web for {company_name}...", 10)
        search_results = search_company(company_name)

        update_status(f"Fetching Wikipedia data for {company_name}...", 20)
        wiki_summary = get_wikipedia_summary(company_name)

        combined_research = f"""
COMPANY: {company_name}

WIKIPEDIA SUMMARY:
{wiki_summary}

WEB SEARCH RESULTS:
{search_results}
        """.strip()

        # Step 2 – Overview
        update_status("Generating company overview...", 35)
        overview = analyze_with_ollama(
            model_name,
            f"""You are a business analyst. Based on the research below, write a concise Company Overview for {company_name}.

Cover:
- What the company does
- Industry & sector
- Scale (revenue, employees, projects if available)
- Geographic presence

Research:
{combined_research}

Be specific and factual. Use 3-4 paragraphs."""
        )
        report_data["overview"] = overview

        # Step 3 – Key Business Info
        update_status("Extracting key business information...", 50)
        biz_info = analyze_with_ollama(
            model_name,
            f"""You are a business analyst. Based on the research below, identify key business information for {company_name}.

Include:
- Major products/services/offerings
- Recent developments or news (last 1-2 years)
- Expansion plans
- Important partnerships, awards, or milestones

Research:
{combined_research}

Use bullet points. Be specific to this company."""
        )
        report_data["biz_info"] = biz_info

        # Step 4 – Challenges
        update_status("Identifying business challenges...", 65)
        challenges = analyze_with_ollama(
            model_name,
            f"""You are a strategic business consultant. Based on the research below about {company_name}, identify specific potential business challenges.

For each challenge:
1. State the challenge clearly
2. Explain the reasoning (why this is a challenge for THIS company)
3. Give the business impact

Categories to cover:
- Operational bottlenecks
- Sales challenges
- Customer experience challenges
- Market/competitive challenges

Research:
{combined_research}

Be highly specific to {company_name}. Avoid generic industry challenges unless you connect them to this company specifically."""
        )
        report_data["challenges"] = challenges

        # Step 5 – AI Opportunities
        update_status("Identifying AI opportunities...", 78)
        ai_opps = analyze_with_ollama(
            model_name,
            f"""You are an AI solutions architect. Based on the research below about {company_name} and the challenges identified, suggest specific AI opportunities.

For each opportunity:
1. Name the AI solution
2. The specific business problem it solves
3. Expected impact/benefit
4. Implementation complexity (Low/Medium/High)

Cover areas like:
- Sales automation & lead scoring
- Customer engagement & chatbots
- Document processing & OCR
- Predictive analytics
- Operations optimization

Research:
{combined_research}

Do NOT give generic answers. Every suggestion must directly address a real challenge specific to {company_name}."""
        )
        report_data["ai_opps"] = ai_opps

        # Step 6 – CEO Pitch
        update_status("Writing personalized CEO pitch...", 90)
        pitch = analyze_with_ollama(
            model_name,
            f"""You are writing a personalized one-page pitch to the CEO of {company_name}.

Write a compelling pitch that includes:
1. Why you reached out to {company_name} specifically (reference their business)
2. Key opportunities you identified (2-3 specific points from research)
3. The AI solutions you recommend and their expected business value
4. A clear call to action

Research about the company:
{combined_research}

Tone: Professional, direct, confident. Address the CEO respectfully.
Length: One page (400-500 words max)."""
        )
        report_data["pitch"] = pitch

        # Done
        progress_bar.progress(100)
        status_placeholder.markdown('<div class="status-box" style="background:#d4edda;border-color:#c3e6cb;">✅ Report generated successfully!</div>', unsafe_allow_html=True)
        time.sleep(0.5)
        status_placeholder.empty()
        progress_bar.empty()

        # ── Display Report ─────────────────────────────────────────────────────
        st.markdown(f"## 📊 Intelligence Report: {company_name}")
        st.markdown(f"*Generated on {time.strftime('%B %d, %Y at %H:%M')}*")
        st.markdown("---")

        with st.expander("🏢 1. Company Overview", expanded=True):
            st.markdown(f'<div class="section-card">{overview}</div>', unsafe_allow_html=True)

        with st.expander("📋 2. Key Business Information", expanded=True):
            st.markdown(f'<div class="section-card biz">{biz_info}</div>', unsafe_allow_html=True)

        with st.expander("⚠️ 3. Potential Business Challenges", expanded=True):
            st.markdown(f'<div class="section-card challenges">{challenges}</div>', unsafe_allow_html=True)

        with st.expander("🤖 4. AI Opportunities", expanded=True):
            st.markdown(f'<div class="section-card ai-opps">{ai_opps}</div>', unsafe_allow_html=True)

        with st.expander("🎯 5. Personalized CEO Pitch", expanded=True):
            st.markdown(f'<div class="section-card pitch">{pitch}</div>', unsafe_allow_html=True)

        # ── Downloads ─────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📥 Download Report")
        dl1, dl2 = st.columns(2)

        md_content = generate_markdown_report(company_name, report_data)
        with dl1:
            st.download_button(
                "📄 Download Markdown",
                data=md_content,
                file_name=f"{company_name.replace(' ', '_')}_report.md",
                mime="text/markdown",
                use_container_width=True
            )

        try:
            pdf_bytes = generate_pdf_report(company_name, report_data)
            with dl2:
                st.download_button(
                    "📑 Download PDF",
                    data=pdf_bytes,
                    file_name=f"{company_name.replace(' ', '_')}_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        except Exception:
            with dl2:
                st.info("Install reportlab for PDF export")

    except Exception as e:
        progress_bar.empty()
        status_placeholder.empty()
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure Ollama is running: `ollama serve` and the model is pulled: `ollama pull llama3.2`")

elif generate_btn and not company_name.strip():
    st.warning("⚠️ Please enter a company name.")
