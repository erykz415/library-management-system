import streamlit as st

from views.history import history_page
from views.home import home_page
from views.login_registration import login_registration_page
from views.my_books import my_books_page
from views.watched import watched_page


def run_app():

    user = st.session_state.get("user")

    if user is None:
        login_registration_page()
        return

    with st.sidebar:
        if st.button("Log out", use_container_width=True):
            st.session_state["user"] = None
            st.rerun()

        with st.sidebar.expander("Account"):
            st.write(f"👤 {user.username}")
            st.caption(f"Role: {user.get_role()}")

        st.divider()
        st.title("Library")

        pages = ["Book Catalog", "History"]
        if user.get_role() in ("student", "lecturer"):
            pages.insert(1, "My books")
            pages.insert(2, "Watched books")

        page = st.sidebar.radio("Navigation", pages)

    if page == "Book Catalog":
        home_page()
    elif page == "My books":
        my_books_page()
    elif page == "Watched books":
        watched_page()
    elif page == "History":
        history_page()
