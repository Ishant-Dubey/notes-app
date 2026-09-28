import streamlit as st
import requests

st.set_page_config(layout="wide")

all_notes = None
if st.session_state.get("logged_in", False):
    token = st.session_state["access_token"]
    all_notes = requests.get(
        "http://127.0.0.1:8000/notes", headers={"Authorization": f"Bearer {token}"}
    )

else:
    st.title("Login Yourself!")

if all_notes:
    notes = all_notes.json()
    columns = st.columns(3)
    for i, note in enumerate(notes):
        with columns[i % 3]:
            with st.container(border=True, width="stretch", height="content"):
                st.markdown(f":blue-background[**{note['title']}**]")
                st.markdown(f":green-background[{note['content']}]")

                c1, c2 = st.columns(2)

                with c1.container(
                    border=False,
                    width="stretch",
                    vertical_alignment="bottom",
                    horizontal_alignment="left",
                ):
                    edit_note = st.button(
                        label="Edit",
                        key=f"edit_{note['id']}",
                        icon=":material/edit:",
                    )

                if edit_note:

                    @st.dialog("Edit")
                    def edit_note_dialog(note=note):
                        title = st.text_input(label="Title", value=note["title"])
                        content = st.text_area(label="Content", value=note["content"])

                        if st.button(
                            "Done",
                            key=f"done_{note['id']}",
                            icon=":material/done_outline:",
                        ):
                            response = requests.put(
                                f"http://127.0.0.1:8000/notes/{note['id']}",
                                json={"title": title, "content": content},
                                headers={"Authorization": f"Bearer {token}"},
                            )

                            if response.status_code == 200:
                                st.rerun()
                            else:
                                st.error(response.json())

                    edit_note_dialog()

                with c2.container(
                    border=False,
                    width="stretch",
                    vertical_alignment="bottom",
                    horizontal_alignment="right",
                ):
                    delete_note = st.button(
                        label="Delete",
                        key=f"del_{note['id']}",
                        icon=":material/delete:",
                    )

                if delete_note:
                    response = requests.delete(
                        f"http://127.0.0.1:8000/notes/{note['id']}",
                        headers={"Authorization": f"Bearer {token}"},
                    )

                    if response.status_code == 200:
                        st.rerun()
                    else:
                        st.error(response.json())

    create_note = st.button(
        "Create Note", key="create_key", icon=":material/add:", icon_position="right"
    )
    if create_note:

        @st.dialog("Create Note")
        def create_note_dialog():
            title = st.text_input("Title")
            content = st.text_area("Content")

            if st.button("Done", key="done_key", icon=":material/done_outline:"):
                response = requests.post(
                    "http://127.0.0.1:8000/notes",
                    json={"title": title, "content": content},
                    headers={"Authorization": f"Bearer {token}"},
                )

                if response.status_code == 201:
                    new_note = response.json()
                    notes.append(new_note)
                    st.rerun()
                else:
                    st.error(response.json())

        create_note_dialog()
