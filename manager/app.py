from models import DatabaseManager, User, Transaction
import streamlit as st
from login_page import Login, Sign_Up

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.name = None
    page_nav = st.navigation([st.Page('login_page.py', title='Login Page')], position='top')
    if not st.session_state.logged_in:
        page_nav.run()

main()