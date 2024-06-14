import streamlit as st
import streamlit.components.v1 as components

from auth import is_logged_in
from navigation import go_home
from integration.connection import post_find_schema_matching, post_find_data_matching, post_generate_erd


def main():
    if not is_logged_in():
        go_home()

    st.title("ERD")
    st.info("This is an experimental feature.")

    response = post_generate_erd(1)
    if response["status_code"] != 200:
        st.error("Failed to generate ERD.")
        return

    for erd in response["erds"]:
        mermaid(erd)


def mermaid(code: str) -> None:
    components.html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=500,
    )

if __name__ == '__main__':
    main()
