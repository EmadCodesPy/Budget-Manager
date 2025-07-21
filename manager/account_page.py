import streamlit as st
from models import User, Transaction

def remove_account():
    if 'delete_flow' not in st.session_state:
        st.session_state.delete_flow = False
    if not st.session_state.delete_flow:
        if st.button('Delete Account', type='primary', icon='🗑️'):
            st.session_state.delete_flow = True
            st.rerun()
    else:
        st.warning('This will :red[Permanently] delete your account')
        st.text_input('Type YES to delete', key='confirm_delete_input')
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button('', icon='🗑️', type='primary'):
                if st.session_state.confirm_delete_input.strip() == 'YES':
                    user = User(st.session_state.username, st.session_state.name)
                    user.delete_account()
                    st.success('Account Deleted')
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    st.session_state.name = None
                    st.session_state.delete_flow = False
                    st.session_state.account = False
                    st.session_state.month = False
                    st.rerun()
                else:
                    st.toast('You must type YES to confirm')
        with col2:
            if st.button('Cancel'):
                st.session_state.delete_flow = False
                st.rerun()

def stat_grid():
    tx = Transaction(st.session_state.username)
    col1,col2,col3 = st.columns([1,1,0.5])
    with col1:
        st.markdown('Total Budget')
    with col2:
        st.markdown('Total Spending')
    with col3:
        st.markdown('Earning - Spending')
    col1, col2, col3 = st.columns([1,1,0.5])
    with col1:
        st.markdown(f'{tx.get_total_budget()}')
    with col2:
        st.markdown(f'{tx.get_total_spending()}')
    with col3:
        st.markdown(f'{(tx.get_total_earning()-tx.get_total_spending())}')

def main():
    user = User(st.session_state.username, st.session_state.name)
    col1,col2 = st.columns([5,2])
    with col1:
        st.markdown('## 👤 Account')
    with col2:
        st.markdown('')
        remove_account()
    st.divider()
    with st.container(border=False):
        st.markdown(f'### **You are signed in as** {st.session_state.username}')
    with st.sidebar:
        overview_button = st.button('Back to Overview')
        if overview_button:
            st.session_state.account = False
            st.rerun()
    st.divider()
    stat_grid()

if __name__ == "__main__":
    main()