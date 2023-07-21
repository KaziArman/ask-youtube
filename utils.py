<<<<<<< HEAD
import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
=======
import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
>>>>>>> 52de17b5fd100f8a16c3380f94ce8b9799d13233
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)