import streamlit as st


def history_page():
    st.title("Action history")

    user = st.session_state["user"]
    library = st.session_state["library"]
    perms = user.get_permissions()

    if "undo_last_action" in perms:
        with st.container(border=True):
            st.subheader("Undo last action")
            if st.button("Undo", use_container_width=True):
                result = library.undo_last(user)
                if result:
                    st.success(result)
                    st.rerun()
        st.divider()

    if "show_history_all" in perms:
        st.subheader("All actions")
        history = library.get_history()
    else:
        st.subheader("Your actions")
        history = library.get_history(user)

    if not history:
        st.info("No actions in history")
        return
    for cmd in reversed(history):
        with st.container(border=True):
            st.write(cmd.describe())
