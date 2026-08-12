"""Evidence Browser — Source provenance and web verification status."""

import streamlit as st

st.set_page_config(page_title="ProcureX — Evidence Browser", layout="wide")

try:
    from app import apply_custom_css, init_session_state, render_common_sidebar
    apply_custom_css()
    init_session_state()
    render_common_sidebar()
except Exception:
    pass

st.markdown("<h1>Evidence <span class='gradient-text'>Browser</span></h1>", unsafe_allow_html=True)
st.markdown("*Source provenance and verification status for all supplier claims.*")

session = st.session_state.get("research_session")

st.markdown("### Fetched Web Source URLs")

if session and session.suppliers:
    all_urls = set()
    for supplier in session.suppliers:
        if supplier.website:
            all_urls.add(supplier.website)
        if supplier.source_urls:
            all_urls.update(supplier.source_urls)

    if all_urls:
        for url in sorted(all_urls):
            st.markdown(f"- [{url}]({url})")
    else:
        st.info("No web source URLs retrieved yet.")
else:
    st.info("No active research session. Complete a research session to view fetched web URLs.")
