import streamlit as st
import pandas as pd
import sqlite3

# ---------------- LOGIN CHECK ---------------- #

if "logged_in" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# ---------------- PAGE UI ---------------- #

st.title("CSV SQL Dashboard")

st.success(f"Welcome {st.session_state.username}")

st.write("Upload CSV file(s) and run SQL queries.")

# ---------------- FILE UPLOAD ---------------- #

uploaded_files = st.file_uploader(
    "Upload CSV Files",
    type=["csv"],
    accept_multiple_files=True
)

# ---------------- DATABASE CONNECTION ---------------- #

conn = sqlite3.connect(":memory:")

uploaded_table_names = []

# ---------------- LOAD CSV TO SQL ---------------- #

if uploaded_files:

    for file in uploaded_files:

        try:
            # Read CSV
            df = pd.read_csv(file)

            # Table name from file name
            table_name = file.name.replace(".csv", "").replace(" ", "_")

            # Save to SQLite
            df.to_sql(table_name, conn, index=False, if_exists="replace")

            uploaded_table_names.append(table_name)

            st.success(f"Loaded table: {table_name}")

            st.write("First 10 Rows")

            st.dataframe(df.head(10))

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- SHOW TABLES ---------------- #

if uploaded_table_names:

    st.divider()

    st.subheader("Available Tables")

    for table in uploaded_table_names:
        st.write(f"• {table}")

    # ---------------- SQL QUERY INPUT ---------------- #

    st.divider()

    st.subheader("Run SQL Query")

    default_query = f"SELECT * FROM {uploaded_table_names[0]} LIMIT 10"

    query = st.text_area(
        "Write SQL Query",
        value=default_query,
        height=150
    )

    # ---------------- RUN QUERY ---------------- #

    if st.button("Run Query"):

        try:
            result = pd.read_sql_query(query, conn)

            st.success("Query Executed Successfully")

            st.dataframe(result)

        except Exception as e:
            st.error(f"SQL Error: {e}")

# ---------------- LOGOUT ---------------- #

st.divider()

if st.button("Logout"):

    st.session_state.clear()

    st.switch_page("app.py")