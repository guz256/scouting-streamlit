import streamlit as st

def mostrar_footer():
    st.markdown("---")
    st.caption("📈 Aplicación de Scouting desarrollada por Guzmán Montgomery")

    st.markdown(
        """
        <div style='text-align: right; font-size: 0.85rem; margin-top: -1rem;'>
            <a href='https://www.linkedin.com/in/guzman-montgomery/' target='_blank'>
                💼 Linkedin: Guzmán Montgomery
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
