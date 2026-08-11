"""Reusable component to display evidence records with status badges."""

import streamlit as st


STATUS_BADGES = {
    "verified": ("🟢", "Verified", "#22c55e"),
    "corroborated": ("🔵", "Corroborated", "#3b82f6"),
    "documented": ("🟦", "Documented", "#06b6d4"),
    "claimed": ("🟡", "Claimed", "#eab308"),
    "conflicting": ("🔴", "Conflicting", "#ef4444"),
    "unknown": ("⚪", "Unknown", "#6b7280"),
}


def get_status_badge(status_value: str) -> str:
    """Return emoji + label for an evidence status."""
    icon, label, _ = STATUS_BADGES.get(status_value, ("⚪", "Unknown", "#6b7280"))
    return f"{icon} {label}"


def get_status_color(status_value: str) -> str:
    """Return color hex for an evidence status."""
    _, _, color = STATUS_BADGES.get(status_value, ("⚪", "Unknown", "#6b7280"))
    return color


def render_evidence_viewer(evidence_graph) -> None:
    """Render evidence graph for a supplier with status badges and contradiction alerts."""
    if not evidence_graph:
        st.info("📭 No evidence collected for this supplier.")
        return

    # Claims grouped by field
    if evidence_graph.claims:
        for field_name, records in evidence_graph.claims.items():
            with st.expander(f"📋 {field_name.replace('_', ' ').title()} ({len(records)} source{'s' if len(records) != 1 else ''})"):
                for record in records:
                    status_str = record.evidence_status.value if hasattr(record.evidence_status, "value") else str(record.evidence_status)
                    badge = get_status_badge(status_str)
                    color = get_status_color(status_str)

                    st.markdown(
                        f"""<div style="background:rgba(19,24,54,0.6); border-left:3px solid {color};
                        padding:0.7rem 1rem; margin:0.3rem 0; border-radius:0 8px 8px 0;">
                        <strong>{badge}</strong> &mdash; <code>{record.value}</code><br>
                        <small>Source: {record.source} &bull; Confidence: {record.confidence:.0%}
                        {f' &bull; <a href="{record.url}" target="_blank">🔗 Link</a>' if record.url else ''}
                        {f' &bull; Retrieved: {record.retrieved_at.strftime("%Y-%m-%d %H:%M")}' if record.retrieved_at else ''}</small>
                        </div>""",
                        unsafe_allow_html=True,
                    )
    else:
        st.info("No evidence claims recorded.")

    # Contradictions
    if evidence_graph.contradictions:
        st.markdown("### ⚠️ Contradictions Detected")
        for contradiction in evidence_graph.contradictions:
            st.warning(
                f"**{contradiction.field_name.replace('_', ' ').title()}**: {contradiction.description}\n\n"
                f"Conflicting values: {', '.join(str(v) for v in contradiction.values)}\n\n"
                f"Sources: {', '.join(contradiction.sources)}"
            )
