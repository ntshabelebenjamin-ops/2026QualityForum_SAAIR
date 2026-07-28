import streamlit as st


def section_title(title, icon="📊"):
    st.markdown(f"## {icon} {title}")


def info_card(title, value, help_text=""):
    st.metric(
        label=title,
        value=value,
        help=help_text
    )


def executive_alert(message, level="info"):
    if level == "success":
        st.success(message)
    elif level == "warning":
        st.warning(message)
    elif level == "error":
        st.error(message)
    else:
        st.info(message)


def page_footer():
    st.markdown("---")
    st.caption(
        "QAInsight AI • AI-Powered Quality Assurance Decision Support System"
    )
