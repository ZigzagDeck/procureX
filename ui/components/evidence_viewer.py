"""Clean evidence viewer component focusing on fetched web sources."""

import streamlit as st
from urllib.parse import urlparse


STATUS_BADGES = {
    "verified": ("🟢", "Verified Source", "#22c55e"),
    "corroborated": ("🔵", "Corroborated Web Data", "#3b82f6"),
    "documented": ("🟦", "Extracted Catalog", "#06b6d4"),
    "claimed": ("🟡", "Web Search Claim", "#eab308"),
    "conflicting": ("🔴", "Conflicting Data", "#ef4444"),
    "unknown": ("⚪", "Unverified", "#6b7280"),
}


def render_evidence_viewer(evidence_graph) -> None:
    """Render evidence graph focusing on fetched websites and claims."""
    if not evidence_graph or not evidence_graph.claims:
        st.info("📭 No web evidence records collected.")
        return

    for field_name, records in evidence_graph.claims.items():
        field_title = field_name.replace("_", " ").title()
        st.markdown(f"#### 🌐 {field_title} Provenance")

        for record in records:
            status_str = record.evidence_status.value if hasattr(record.evidence_status, "value") else str(record.evidence_status)
            icon, label, color = STATUS_BADGES.get(status_str, ("⚪", "Unverified", "#6b7280"))
            domain = urlparse(record.url).netloc if record.url else record.source

            st.markdown(
                f"""<div class="glass-card" style="padding: 1rem; margin-bottom: 0.8rem; border-left: 3px solid {color};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; color:{color};">{icon} {label}</span>
                    <span style="color:#94a3b8; font-size:0.8rem;">Confidence: {record.confidence:.0%}</span>
                </div>
                <div style="margin: 6px 0;">
                    <strong style="color:white;">Value:</strong> <code style="background:rgba(56,189,248,0.1); color:#38bdf8; padding:2px 8px; border-radius:4px;">{record.value}</code>
                </div>
                {f'<div style="color:#cbd5e1; font-size:0.85rem; font-style:italic; margin:4px 0;">"{record.raw_snippet}"</div>' if record.raw_snippet else ''}
                <div style="font-size:0.8rem; color:#64748b; margin-top:4px;">
                    Source: {domain} {f' &bull; <a href="{record.url}" target="_blank" style="color:#38bdf8;">Open Source Link 🔗</a>' if record.url else ''}
                </div>
                </div>""",
                unsafe_allow_html=True,
            )

    if evidence_graph.contradictions:
        st.markdown("#### ⚠️ Contradiction Signals")
        for c in evidence_graph.contradictions:
            st.warning(f"**{c.field_name.replace('_', ' ').title()}**: {c.description} (Sources: {', '.join(c.sources)})")
