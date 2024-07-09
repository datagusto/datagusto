import streamlit as st
from enum import Enum

class Page(str, Enum):
    HOME = 'main'
    DATA_SOURCES = '20_Data_Sources'
    WORKSHEETS = '30_Worksheets'
    DATA_MATCHING = '40_Data_Matching'
    DATA_ANALYSIS = '50_Data_Analysis'
    LOGOUT = '99_Log_out'


def switch_page(page_name: Page):
    page_path = f'{page_name.value}.py'
    if page_name != Page.HOME:
        page_path = f'pages/{page_path}.py'
    st.switch_page(page_path)


def go_home():
    switch_page(Page.HOME)
