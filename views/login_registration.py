import streamlit as st


def login_registration_page():
    st.title("Library System")
    st.write("Log in or register to use the library.")

    # tab_login, tab_register = st.tabs(["Login", "Registration"])
    _, col, _ = st.columns([1, 2, 1])
    with col:
        tab_login, tab_register = st.tabs(["Login", "Register"])
        with tab_login:
            _login_form()

        with tab_register:
            _register_form()


def _login_form():
    with st.form("login_form"):
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password")
            return

        auth = st.session_state["auth"]
        user = auth.login(username, password)

        if user is None:
            st.error("Incorrect username or password")
        else:
            st.session_state["user"] = user
            st.success(f"Welcome {user.first_name}!")
            st.rerun()


def _register_form():
    with st.form("register_form"):
        st.subheader("Register")

        role = st.selectbox(
            "Role",
            ["student", "lecturer", "librarian"],
        )

        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First name")
        with col2:
            last_name = st.text_input("Last name")

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password2 = st.text_input("Repeat password", type="password")

        submitted = st.form_submit_button("Register", use_container_width=True)

    if submitted:
        if not all([first_name, last_name, username, email, password, password2]):
            st.error("Please enter all fields")
            return

        if password != password2:
            st.error("Passwords do not match")
            return

        auth = st.session_state["auth"]
        user = auth.register(role, first_name, last_name, username, email, password)

        st.success(f"Account created! You can now log in, {user.first_name}!")
