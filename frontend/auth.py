import streamlit as st

from integration.user import signup, login
from navigation import Page, switch_page


def is_logged_in():
    return 'access_token' in st.session_state


def handle_signup():
    username = st.session_state.signup_username
    password = st.session_state.signup_password
    if not username or not password:
        st.error('Username and password are required.')
        return

    # send singup request to backend
    response = signup(username, password)

    if response['status_code'] != 201:
        st.error(response.get('detail', 'Failed to sign up.'))
        return
    st.success('Successfully signed up! You can now log in.')
    return


def handle_login():
    username = st.session_state.login_username
    password = st.session_state.login_password
    if not username or not password:
        st.error('Username and password are required.')
        return

    # send login request to backend
    response = login(username, password)

    if response['status_code'] != 200:
        st.error(response.get('detail', 'Invalid username or password.'))
    else:
        st.session_state['user'] = username
        st.session_state['access_token'] = response.get('access_token')
        st.success(f'Welcome back, {username}!')


def handle_logout():
    if 'user' in st.session_state:
        del st.session_state['user']
        del st.session_state['access_token']
    switch_page(Page.HOME)


def show_login_page():
    with st.form("Login", clear_on_submit=True):
        st.text_input('Username', key='login_username')
        st.text_input('Password', type='password', key='login_password')
        submit_button = st.form_submit_button('Login', on_click=handle_login)

def show_signup_page():
    with st.form("Signup", clear_on_submit=True):
        st.text_input('New Username', key='signup_username')
        st.text_input('New Password', type='password', key='signup_password')
        signup_button = st.form_submit_button('Signup', on_click=handle_signup)

def show_auth_page():
    tab1, tab2 = st.tabs(["Login", "Signup"])
    with tab1:
        show_login_page()
    with tab2:
        show_signup_page()

def show_logout_page():
    st.write('Are you sure you want to log out?')
    if st.button('Log out'):
        handle_logout()

def get_user_name():
    if 'user' in st.session_state:
        return st.session_state['user']
    return None
