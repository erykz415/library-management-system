import streamlit as st
from models.library_database import LibraryDatabase
from views.home import book_card


def watched_page():
    st.title("Watched books")
    user = st.session_state["user"]
    library = st.session_state["library"]

    all_books = LibraryDatabase().list_books()

    watched = [b for b in all_books if user in b.get_observers()]

    if not watched:
        st.info("You are not watching any books")
        return

    st.write(f"Watched books: {len(watched)}")
    st.divider()

    for book in watched:
        book_card(book, user, library)
