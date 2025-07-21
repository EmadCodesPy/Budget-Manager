from models import DatabaseManager, User, Transaction
import streamlit as st
from login_page import Login, Sign_Up
import datetime

def sidebar():
    with st.sidebar:
        st.markdown(f'**You are signed in as** {st.session_state.username}')
        account = st.sidebar.button('👤 Account')
        if account:
            pass
        with st.container(border=True):
            st.markdown('### Add Transaction' )
            name = st.text_input('Name', placeholder='...')
            type_tx = st.selectbox('Type of transaction', options=('Spending', 'Earning'))
            amount = st.number_input('Amount',min_value=0.00, placeholder='$$$', step=0.01,)
            submit = st.button('Add')
            if submit:
                if amount and type_tx and name:
                    if amount == 0:
                        pass
                    tx = Transaction(st.session_state.username)
                    tx.add_tx(name=name, type=type_tx, amount=amount)
                    st.success('Transaction added')
                else:
                    st.info('Please fill in all fields')

def page():
    months = [datetime.date(2025,m,1).strftime('%B') for m in range(1,13)]
    selected_month = st.selectbox(label='', options=months)
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.name = None
    page_nav = st.navigation([st.Page('login_page.py', title='Login Page')], position='top')
    if not st.session_state.logged_in:
        page_nav.run()
    else:
        sidebar()
        pass

if __name__ == '__main__':
    page()
    #main()
    pass