import streamlit as st
import bcrypt

from db import User, Session
from navigation import Page, switch_page


def is_logged_in():
    return 'user' in st.session_state


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def handle_signup():
    username = st.session_state.signup_username
    password = st.session_state.signup_password
    if not username or not password:
        st.error('Username and password are required.')
        return
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user:
        st.error('Username already exists.')
        return
    hashed_password = hash_password(password)
    new_user = User(username=username, password_hash=hashed_password)
    session.add(new_user)
    session.commit()
    st.success('Successfully signed up! You can now log in.')

def handle_login():
    username = st.session_state.login_username
    password = st.session_state.login_password
    if not username or not password:
        st.error('Username and password are required.')
        return
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user and check_password(password, user.password_hash):
        st.session_state['user'] = username
        st.session_state['user_id'] = user.id
        st.success(f'Welcome back, {username}!')
    else:
        st.error('Invalid username or password.')

def handle_logout():
    if 'user' in st.session_state:
        del st.session_state['user']
        del st.session_state['user_id']
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
        return st.session_state.user
    return None

def get_user_id():
    if 'user_id' in st.session_state:
        return st.session_state.user_id
    return None
