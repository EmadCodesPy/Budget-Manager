import streamlit as st
from models import User
import time

def Login():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if username == '' or password == '':
            st.error('Please fill in a username and password')
        elif User.login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.name = username
            st.success('Logged in succesfully')
            time.sleep(1)
            st.rerun()
        else:
            st.error('Invalid username or password')

def Sign_Up():
    st.title('Sign Up')
    username = st.text_input('Userrname')
    name = st.text_input('Full name')
    password = st.text_input('Password', type='password')
    if st.button('Create Account'):
        try:
            User.sign_up(username, name, password)
            st.success('Account Created')
            time.sleep(1)
        except:
            st.warning('Username already in use :(')

if __name__ == '__main__':
    pg = st.navigation([Login, Sign_Up], position='top')
    pg.run()