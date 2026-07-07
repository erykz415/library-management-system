import streamlit as st
from controllers.app_controller import run_app
from controllers.auth_service import AuthService
from controllers.library_proxy import LibraryProxy
from controllers.library_service import LibraryService
from models.seed import seed_books, seed_users

st.set_page_config(page_title="Library", page_icon="📚", layout="wide")

if "auth" not in st.session_state:
    st.session_state["auth"] = AuthService()
    seed_users(st.session_state["auth"])

if "library" not in st.session_state:
    st.session_state["library"] = LibraryProxy(LibraryService())
    seed_books()

if "user" not in st.session_state:
    st.session_state["user"] = None
    # st.session_state.user = st.session_state.auth.login("j_smith", "pass1234")


if __name__ == "__main__":
    run_app()
