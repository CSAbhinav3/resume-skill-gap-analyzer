import asyncio
import sys
from pathlib import Path

import streamlit as st

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.pdf_ingestion import ingest_pdf, PDFIngestionError
from app.services.skill_extractor import extract_skills
from app.services.taxonomy_engine import taxonomy_index
from app.services.gap_analyzer import analyze_gap
from app.services.roadmap_generator import generate_roadmap
from app.config import settings
import os
from pathlib import Path

# Auto-build taxonomy if embeddings don't exist
# Handles Streamlit Cloud cold starts
if not Path("data/taxonomy/embeddings.npy").exists():
    import subprocess
    subprocess.run(
        ["python", "scripts/build_taxonomy.py"],
        check=True
    )

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1F4E79;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2E75B6;
        border-bottom: 2px solid #2E75B6;
        padding-bottom: 0.3rem;
        margin-bottom: 1rem;
    }
    .skill-tag {
        display: inline-block;
        background: #EBF3FB;
        color: #1F4E79;
        padding: 2px 10px;
        border-radius: 12px;
        margin: 2px;
        font-size: 0.85rem;
    }
    .gap-tag {
        display: inline-block;
        background: #FFF3CD;
        color: #856404;
        padding: 2px 10px;
        border-radius: 12px;
        margin: 2px;
        font-size: 0.85rem;
    }
    .metric-card {
        background: #F5F9FF;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #CCDDEE;
    }
    .week-card {
        background: #FAFAFA;
        border-left: 4px solid #2E75B6;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 0 8px 8px 0;
    }
    .resource-link {
        color: #2E75B6;
        text-decoration: none;
        font-size: 0.9rem;
    }
    .stProgress > div > div > div {
        background-color: #2E75B6;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOAD TAXONOMY (cached — runs once)
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading taxonomy index...")
def load_taxonomy():
    taxonomy_index.load()
    return taxonomy_index


# ─────────────────────────────────────────────
# ASYNC RUNNER
# ─────────────────────────────────────────────
def run_async(coro):
    """Run async coroutine in Streamlit's sync context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/resume.png", width=80)
    st.markdown("## Resume Skill Gap Analyzer")
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("""
1. 📄 **Upload** your PDF resume
2. 🎯 **Enter** your target role
3. 🔍 **Analyze** skill gaps
4. 🗺️ **Get** your 90-day roadmap
    """)
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
- **LLM:** Groq llama-3.3-70b
- **Embeddings:** all-MiniLM-L6-v2
- **Taxonomy:** 217 skills from 750 job postings
- **Similarity:** Cosine similarity
    """)
    st.markdown("---")
    st.markdown(
        "Built by **C S Abhinav** — Altruist Technologies",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────
st.markdown('<p class="main-title">🎯 Resume Skill Gap Analyzer</p>',
            unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Upload your resume, enter your target role, '
    'and get a personalised 30/60/90-day learning roadmap.</p>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"],
        help="Upload a PDF resume to analyze skill gaps"
    )

with col2:
    target_role = st.text_input(
        "Target Role",
        placeholder="e.g. Data Scientist",
        help="Enter the job role you are targeting. "
             "Leave blank to analyze against full taxonomy."
    )
    st.markdown("**Example roles:**")
    role_cols = st.columns(2)
    roles = ["Data Scientist", "ML Engineer", "Backend Engineer",
             "DevOps Engineer", "Data Analyst", "Full Stack Engineer"]
    for i, role in enumerate(roles):
        if role_cols[i % 2].button(role, key=f"role_{i}", use_container_width=True):
            target_role = role
            st.rerun()

st.markdown("---")

# ─────────────────────────────────────────────
# ANALYZE BUTTON
# ─────────────────────────────────────────────
analyze_clicked = st.button(
    "🔍 Analyze My Resume",
    type="primary",
    use_container_width=True,
    disabled=uploaded_file is None
)

if uploaded_file is None:
    st.info("👆 Upload a PDF resume to get started.")
    st.stop()

if not analyze_clicked:
    st.stop()

# ─────────────────────────────────────────────
# PIPELINE EXECUTION
# ─────────────────────────────────────────────
load_taxonomy()

progress = st.progress(0, text="Starting analysis...")
status   = st.empty()

# Step 1: PDF Ingestion
status.info("📄 Extracting text from PDF...")
progress.progress(10, text="Extracting PDF text...")

try:
    file_bytes = uploaded_file.read()
    ingested   = ingest_pdf(file_bytes)
except PDFIngestionError as e:
    st.error(f"❌ PDF Error: {e}")
    st.stop()

progress.progress(25, text="PDF extracted successfully.")

# Step 2: Skill Extraction
status.info("🤖 Extracting skills with LLM...")
progress.progress(35, text="Extracting skills (LLM call)...")

try:
    skills_data = run_async(extract_skills(ingested["clean_text"]))
except Exception as e:
    st.error(f"❌ Skill extraction failed: {e}")
    st.stop()

all_skills = (
    skills_data["technical_skills"] +
    skills_data["tools"] +
    skills_data["soft_skills"]
)
progress.progress(55, text="Skills extracted.")

# Step 3: Gap Analysis
status.info("📊 Analyzing skill gaps...")
progress.progress(65, text="Running gap analysis...")

try:
    gap_result = analyze_gap(all_skills, target_role=target_role or None)
except Exception as e:
    st.error(f"❌ Gap analysis failed: {e}")
    st.stop()

progress.progress(75, text="Gap analysis complete.")

# Step 4: Roadmap Generation
status.info("🗺️ Generating your learning roadmap...")
progress.progress(85, text="Generating roadmap (LLM call)...")

try:
    roadmap = run_async(generate_roadmap(gap_result, target_role=target_role or None))
except Exception as e:
    st.error(f"❌ Roadmap generation failed: {e}")
    st.stop()

progress.progress(100, text="Analysis complete!")
status.success("✅ Analysis complete!")

st.markdown("---")

# ─────────────────────────────────────────────
# RESULTS — OVERVIEW METRICS
# ─────────────────────────────────────────────
st.markdown('<p class="section-header">📊 Overview</p>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric(
    "Overall Match",
    f"{gap_result.overall_match_score:.1%}",
    help="How well your resume matches the target role taxonomy"
)
m2.metric(
    "Skills Extracted",
    len(all_skills),
    help="Total skills found in your resume"
)
m3.metric(
    "Skills Matched",
    len(gap_result.present_skills),
    help="Skills in your resume that match the taxonomy"
)
m4.metric(
    "Skill Gaps",
    len(gap_result.missing_skills),
    help="Skills missing from your resume for this role"
)

if target_role:
    st.caption(
        f"Analysis filtered to **{gap_result.filtered_taxonomy_size}** skills "
        f"relevant to **{target_role}** "
        f"(from 217-skill taxonomy)"
    )

st.markdown("---")

# ─────────────────────────────────────────────
# RESULTS — EXTRACTED SKILLS
# ─────────────────────────────────────────────
st.markdown('<p class="section-header">✅ Your Current Skills</p>',
            unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    f"⚙️ Technical ({len(skills_data['technical_skills'])})",
    f"🛠️ Tools ({len(skills_data['tools'])})",
    f"🤝 Soft Skills ({len(skills_data['soft_skills'])})",
])

with tab1:
    if skills_data["technical_skills"]:
        tags = " ".join(
            f'<span class="skill-tag">{s}</span>'
            for s in skills_data["technical_skills"]
        )
        st.markdown(tags, unsafe_allow_html=True)
    else:
        st.caption("No technical skills extracted.")

with tab2:
    if skills_data["tools"]:
        tags = " ".join(
            f'<span class="skill-tag">{s}</span>'
            for s in skills_data["tools"]
        )
        st.markdown(tags, unsafe_allow_html=True)
    else:
        st.caption("No tools extracted.")

with tab3:
    if skills_data["soft_skills"]:
        tags = " ".join(
            f'<span class="skill-tag">{s}</span>'
            for s in skills_data["soft_skills"]
        )
        st.markdown(tags, unsafe_allow_html=True)
    else:
        st.caption("No soft skills extracted.")

st.markdown("---")

# ─────────────────────────────────────────────
# RESULTS — SKILL GAPS
# ─────────────────────────────────────────────
st.markdown('<p class="section-header">⚠️ Skill Gaps (Ranked by Priority)</p>',
            unsafe_allow_html=True)

if gap_result.missing_skills:
    gap_col1, gap_col2 = st.columns([3, 2])

    with gap_col1:
        import pandas as pd
        gap_df = pd.DataFrame([
            {
                "Rank":     s.priority_rank,
                "Skill":    s.taxonomy_skill_name,
                "Category": s.category.replace("_", " ").title(),
                "Relevance Score": f"{s.similarity_score:.3f}",
            }
            for s in gap_result.missing_skills
        ])
        st.dataframe(
            gap_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn(width="small"),
                "Relevance Score": st.column_config.ProgressColumn(
                    min_value=0, max_value=1, format="%.3f"
                ),
            }
        )

    with gap_col2:
        st.markdown("**Gap Skills:**")
        tags = " ".join(
            f'<span class="gap-tag">#{s.priority_rank} {s.taxonomy_skill_name}</span>'
            for s in gap_result.missing_skills[:10]
        )
        st.markdown(tags, unsafe_allow_html=True)
else:
    st.success("🎉 No skill gaps found! Your resume covers the full taxonomy.")

st.markdown("---")

# ─────────────────────────────────────────────
# RESULTS — ROADMAP
# ─────────────────────────────────────────────
st.markdown('<p class="section-header">🗺️ Your 30/60/90 Day Learning Roadmap</p>',
            unsafe_allow_html=True)

phase_colors = {
    "30_day": "🟢",
    "60_day": "🟡",
    "90_day": "🔴",
}
phase_labels = {
    "30_day": "30-Day Plan — Foundation",
    "60_day": "60-Day Plan — Intermediate",
    "90_day": "90-Day Plan — Advanced",
}

for phase in roadmap.get("phases", []):
    phase_name = phase.get("phase", "")
    phase_goal = phase.get("goal", "")
    icon       = phase_colors.get(phase_name, "⚪")
    label      = phase_labels.get(phase_name, phase_name)

    with st.expander(f"{icon} {label} — {phase_goal}", expanded=phase_name == "30_day"):
        weeks = phase.get("weeks", [])
        for week in weeks:
            week_num = week.get("week", "")
            focus    = week.get("focus", "")
            goal     = week.get("goal", "")
            topics   = week.get("topics", [])
            resources = week.get("resources", [])

            st.markdown(
                f'<div class="week-card">'
                f'<strong>Week {week_num}: {focus}</strong><br>'
                f'<span style="color:#555; font-size:0.9rem;">🎯 {goal}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            if topics:
                st.markdown("**Topics:**")
                for t in topics:
                    st.markdown(f"  - {t}")

            if resources:
                st.markdown("**Resources:**")
                for r in resources:
                    # Parse "Title — Platform — URL (Free/Paid)"
                    parts = r.split(" — ")
                    if len(parts) >= 3:
                        title    = parts[0]
                        platform = parts[1]
                        url_part = parts[2]
                        url      = url_part.split(" ")[0]
                        free     = "(Free)" in r
                        badge    = "🆓" if free else "💰"
                        st.markdown(
                            f"  {badge} [{title}]({url}) — *{platform}*"
                        )
                    else:
                        st.markdown(f"  - {r}")

            st.markdown("")

st.markdown("---")

# ─────────────────────────────────────────────
# WEEKLY BREAKDOWN TABLE
# ─────────────────────────────────────────────
with st.expander("📅 Full Weekly Breakdown"):
    weekly = roadmap.get("weekly_breakdown", [])
    if weekly:
        import pandas as pd
        weekly_df = pd.DataFrame([
            {
                "Week":  w.get("week"),
                "Phase": w.get("phase", "").replace("_", " ").title(),
                "Focus": w.get("focus", ""),
                "Goal":  w.get("goal", ""),
            }
            for w in weekly
        ])
        st.dataframe(weekly_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# DOWNLOAD RESULTS
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 💾 Download Results")

import json
results_json = {
    "resume_file":      uploaded_file.name,
    "target_role":      target_role or "General",
    "extracted_skills": {
        "technical_skills": skills_data["technical_skills"],
        "tools":            skills_data["tools"],
        "soft_skills":      skills_data["soft_skills"],
    },
    "gap_analysis": {
        "overall_match_score":   gap_result.overall_match_score,
        "filtered_taxonomy_size": gap_result.filtered_taxonomy_size,
        "missing_skills": [
            {
                "rank":  s.priority_rank,
                "skill": s.taxonomy_skill_name,
                "score": s.similarity_score,
            }
            for s in gap_result.missing_skills
        ],
    },
    "roadmap": roadmap,
}

st.download_button(
    label="⬇️ Download Full Report (JSON)",
    data=json.dumps(results_json, indent=2),
    file_name=f"skill_gap_report_{target_role or 'general'}.json",
    mime="application/json",
    use_container_width=True,
)