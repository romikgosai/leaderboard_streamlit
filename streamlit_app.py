import streamlit as st
import pandas as pd

# Function to validate login credentials
def validate_login(username, password):
    users = pd.read_csv('users.csv')
    if any((users['username'].str.lower() == username) & (users['password'].str.lower() == password)):
        return True
    return False

# Function to display the input form
def input_form():
    st.title("Input Details")
    category = st.selectbox("Select Category", ["Classification", "Regression"])
    if category == "Classification":
        score_label = "F1 Score"
        csv_file = 'classification_leaderboard.csv'
    else:
        score_label = "R2 Score"
        csv_file = 'regression_leaderboard.csv'
    score = st.number_input(score_label, min_value=0.0, max_value=1.0, step=0.01)
    submit_button = st.button("Submit")
    if submit_button:
        if category and score >= 0:
            # Append the data to the appropriate CSV file
            leaderboard = pd.read_csv(csv_file)
            if category == "Classification":
                new_data = pd.DataFrame({
                    "username": [st.session_state['username']],
                    "F1 score": [score]
                })
            else:
                new_data = pd.DataFrame({
                    "username": [st.session_state['username']],
                    "r2 score": [score]
                })
            leaderboard = pd.concat([leaderboard, new_data])
            leaderboard.to_csv(csv_file, index=False)
            st.success("Submitted successfully!")

# Function to display the leaderboard
def show_leaderboard():
    st.title("Leaderboard")
    category = st.selectbox("Select Category to View", ["Classification", "Regression"])
    if category == "Classification":
        csv_file = 'classification_leaderboard.csv'
        leaderboard = pd.read_csv(csv_file)
        leaderboard = leaderboard.sort_values(by='F1 score', ascending=False).reset_index(drop=True)
        leaderboard.reset_index(drop=True, inplace=True)
        leaderboard.index += 1
        st.table(leaderboard)
    else:
        csv_file = 'regression_leaderboard.csv'
        leaderboard = pd.read_csv(csv_file)
        leaderboard = leaderboard.sort_values(by='r2 score', ascending=False)
        leaderboard.reset_index(drop=True, inplace=True)
        leaderboard.index += 1
        st.table(leaderboard)

# Main app
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.title("Login Page")
        username = st.text_input("Username (Full Name)")
        password = st.text_input("Password (Roll: e.g. KCE078BCT001)", type='password')
        login_button = st.button("Login")

        if login_button:
            if validate_login(username.lower(), password.lower()):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox("Choose a page", ["Input Details", "Leaderboard"])
        logout_button = st.sidebar.button("Logout")

        if logout_button:
            st.session_state['logged_in'] = False
            st.experimental_rerun()

        if page == "Input Details":
            input_form()
        elif page == "Leaderboard":
            show_leaderboard()

if __name__ == "__main__":
    main()
