from typing import Literal, cast

import streamlit as st

from controllers.book import Book
from models.library_database import LibraryDatabase

BadgeColor = Literal[
    "red", "orange", "yellow", "blue", "green", "violet", "gray", "grey", "primary"
]


def home_page():
    st.title("Books catalog")

    user = st.session_state["user"]
    library = st.session_state["library"]

    books = LibraryDatabase().list_books()

    if not books:
        st.info("No books available")
    else:
        st.write(f"{len(books)} books found")
        st.divider()
        for book in books:
            book_card(book, user, library)

    perms = user.get_permissions()
    if "add_book" in perms:
        st.divider()
        _librarian_panel(library, user)


def book_card(book, user, library):
    perms = user.get_permissions()
    state = book.get_state()

    _badge_map: dict[str, tuple[BadgeColor, str]] = {
        "available": ("green", "Available"),
        "borrowed": ("red", "Borrowed"),
        "reserved": ("blue", "Reserved"),
    }
    state_badge = cast(tuple[BadgeColor, str], _badge_map.get(state, ("gray", state)))

    with st.container(border=True):
        col_cover, col_info, col_actions = st.columns([1.2, 4, 1.5])
        with col_cover:
            if book.cover_url:
                st.image(book.cover_url, width="content")
            else:
                st.markdown("No cover available")
        with col_info:
            st.markdown(
                f"""
                    <div style="font-size:24px; font-weight:bold;">
                    {book.title}
                </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(f"***{book.author}***")

            meta = []

            if book.genre:
                meta.append(f"<div><b>Genre:</b> {book.genre}</div>")
            if book.published_year:
                meta.append(
                    f"<div><b>Year of publishing:</b> {str(book.published_year)}</div>"
                )
            meta.append(f"<div><b>ISBN:</b> {book.isbn}</b>")

            st.markdown(
                f"""
                <div style="
                    margin-top:-15px;
                    margin-bottom:10px;
                    color: gray;
                    font-size: 0.9rem;
                    line-height: 1.35;
                    line-spacing: 1;
                ">
                    {"".join(meta)}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.badge(state_badge[1], color=state_badge[0])

            if book.description:
                with st.expander("Description"):
                    st.write(book.description)

        with col_actions:
            isbn = book.isbn
            st.write("")

            if (
                state == "available"
                and "borrow_book" in perms
                or state == "reserved"
                and book.reserved_by == user
            ):
                if st.button(
                    "borrow",
                    key=f"borrow_{isbn}",
                    use_container_width=True,
                    type="primary",
                ):
                    library.borrow_book(isbn, user)
                    st.success(f"You borrowed {book.title}")
                    st.rerun()

            if state == "available" and "reserve_book" in perms:
                if st.button(
                    "reserve", key=f"reserve_{isbn}", use_container_width=True
                ):
                    library.reserve_book(isbn, user)
                    st.success(f"You reserved {book.title}")
                    st.rerun()

            if (
                state == "borrowed"
                and book.borrowed_by == user
                and "return_book" in perms
            ):
                if st.button("return", key=f"return_{isbn}", use_container_width=True):
                    library.return_book(isbn, user)
                    st.info(f"You returned {book.title}")
                    st.rerun()

            if (
                state in ("borrowed", "reserved")
                and book.borrowed_by != user
                and book.reserved_by != user
            ):
                if user.get_role() != "librarian":
                    if st.button(
                        "Observe", key=f"observe_{isbn}", use_container_width=True
                    ):
                        library.observe_book(isbn, user)
                        st.info(f"You observe {book.title}")
                        st.rerun()


def _librarian_panel(library, user):
    st.subheader("Librarian panel")

    tab_add, tab_import, tab_manage = st.tabs(
        ["Add book", "Import book", "Manage books"]
    )

    with tab_add:
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            isbn = st.text_input("ISBN")
            genre = st.text_input("Genre")
            published_year = st.number_input(
                "Year of publishing", min_value=1000, max_value=2050, value=2026, step=1
            )
            description = st.text_input("Description")
            submitted = st.form_submit_button("Submit", use_container_width=True)
        if submitted:
            if not all([title, author, isbn, genre, published_year]):
                st.error("Fill in all fields")
            else:
                library.add_book(
                    Book(
                        title,
                        author,
                        isbn,
                        description=description,
                        genre=genre,
                        published_year=published_year,
                    ),
                    user,
                )
                st.success(f"Added: {title}")
                st.rerun()

    with tab_import:
        with st.form("import_book_form"):
            isbn_ext = st.text_input("ISBN from external database")
            submitted2 = st.form_submit_button("Submit", use_container_width=True)
        if submitted2:
            library.import_book_from_external_db(isbn_ext, user)
            st.rerun()

    with tab_manage:
        books = LibraryDatabase().list_books()
        if not books:
            st.info("No books available")
        for book in books:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{book.title} ({book.isbn})")
            with col2:
                if st.button(
                    "Remove", key=f"remove_{book.isbn}", use_container_width=True
                ):
                    library.remove_book(book.isbn, user)
                    st.rerun()
            with col3:
                if st.button("Edit", key=f"edit_{book.isbn}", use_container_width=True):
                    st.session_state["editing"] = book.isbn

        editing_book = st.session_state.get("editing")
        if editing_book:
            book_to_edit = LibraryDatabase().get_book(editing_book)
            if book_to_edit:
                with st.form(f"edit_book_form_{book_to_edit.isbn}"):
                    st.write(f"You are now editing {book_to_edit.title}")
                    new_title = st.text_input("New title", value=book_to_edit.title)
                    new_author = st.text_input("New author", value=book_to_edit.author)
                    new_description = st.text_input(
                        "New description", value=book_to_edit.description
                    )
                    new_genre = st.text_input("New genre", value=book_to_edit.genre)
                    new_year_published = st.number_input(
                        "New year of publishing", min_value=1000, max_value=2050
                    )
                    save = st.form_submit_button("Save")
                if save:
                    library.update_book(
                        editing_book,
                        user,
                        new_title,
                        new_author,
                        new_description,
                        new_genre,
                        new_year_published,
                    )
                    st.session_state.pop("editing")
                    st.success(f"Edited {book_to_edit.title}")
                    st.rerun()
