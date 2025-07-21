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
                    tx.add_tx(name=name, type=type_tx, amount=amount, month=st.session_state.month)
                    st.success('Transaction added')
                else:
                    st.info('Please fill in all fields')

def page():
    tx = Transaction(st.session_state.username)
    months = tx.get_months()
    if not months:
        st.warning('Head to your account page to allocate a budget')
    selected_month = st.selectbox(label='', options=months)
    st.session_state.month = selected_month
    tx = Transaction(st.session_state.username)
    monthly_budget = round(tx.get_monthly_budget(selected_month),1)
    if monthly_budget > 0:
        st.markdown(f'### {monthly_budget}')
    elif monthly_budget <= 0:
        st.markdown(f'### :red[{monthly_budget}]')
    

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.name = None
        st.session_state.month = None
    page_nav = st.navigation([st.Page('login_page.py', title='Login Page')], position='top')
    if not st.session_state.logged_in:
        page_nav.run()
    else:
        sidebar()
        page()
        pass

if __name__ == '__main__':
    main()
    pass