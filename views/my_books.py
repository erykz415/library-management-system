import streamlit as st
from models.library_database import LibraryDatabase
from views.home import book_card


def my_books_page():
    st.title("My Books")

    user = st.session_state["user"]
    library = st.session_state["library"]

    all_books = LibraryDatabase().list_books()

    borrowed = [b for b in all_books if b.borrowed_by == user]
    reserved = [b for b in all_books if b.reserved_by == user]

    st.subheader(f"Borrowed Books: {len(borrowed)}")
    if not borrowed:
        st.info("You have no borrowed books")

    for book in borrowed:
        book_card(book, user, library)

    if "reserve_book" in user.get_permissions():
        st.subheader(f"Reserved Books: {len(reserved)}")

        if not reserved:
            st.info("You have no reserved books")

        for book in reserved:
            book_card(book, user, library)
