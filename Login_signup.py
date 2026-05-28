import streamlit as st
import pandas as pd
import os

FILE_NAME = "users.xlsx"

# Create Excel file if not exists
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Role", "Username", "Password"])
    df.to_excel(FILE_NAME, index=False)

# Load users
def load_users():
    return pd.read_excel(FILE_NAME)

# Save new user
def save_user(role, username, password):
    df = load_users()

    new_user = pd.DataFrame({
        "Role": [role],
        "Username": [username],
        "Password": [password]
    })

    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(FILE_NAME, index=False)

# Check existing user
def user_exists(username):
    df = load_users()
    return username in df["Username"].values

# Validate login
def validate_login(role, username, password):
    df = load_users()

    user = df[
        (df["Role"] == role) &
        (df["Username"] == username) &
        (df["Password"] == password)
    ]

    return not user.empty


# ---------------- UI ---------------- #

st.title("Login System")

menu = st.sidebar.selectbox("Menu", ["Signup", "Login"])

# SIGNUP
if menu == "Signup":

    st.subheader("Create Account")

    role = st.selectbox("Role", ["User", "Administrator"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):

        if username == "" or password == "":
            st.warning("Fill all fields")

        elif user_exists(username):
            st.error("Username already exists!")

        else:
            save_user(role, username, password)
            st.success("Signup Successful")


# LOGIN
elif menu == "Login":

    st.subheader("Login")

    role = st.selectbox("Login As", ["User", "Administrator"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if validate_login(role, username, password):

            # Save login session
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role

            st.success("Login Successful!")

            # Redirect to dashboard page
            st.switch_page("pages/dashboard.py")

        else:
            st.error("Invalid Credentials")