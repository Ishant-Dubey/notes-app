import streamlit as st
import requests
from config import BACKEND_URL

st.markdown("<h1 style='text-align: center;'>Notes App</h1>", unsafe_allow_html=True)
left, center, right = st.columns([1, 2, 1])
with center:
    with st.container(border=True, width="content"):
        st.write("Login")

        email = st.text_input(
            label="Enter your email",
            type="email",
            placeholder="johndoe@example.com",
            width=325,
        )
        password = st.text_input(
            label="Enter your password",
            type="password",
            placeholder="password",
            width=325,
        )

        if st.button("Login", use_container_width=True, icon=":material/login:"):
            response = requests.post(
                f"{BACKEND_URL}/login", json={"email": email, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state["access_token"] = data["session"]["access_token"]
                st.session_state["logged_in"] = True
                st.success("Login successful")
            else:
                st.error(f"Login failed: {response.text}")
