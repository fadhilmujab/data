from itertools import cycle
import streamlit as st
from utils.cards import link_card
from streamlit_extras.badges import badge

@st.experimental_singleton
def reduce_top_padding():
    return st.markdown("""
        <style>
            .css-18e3th9 {
                padding-top: 0rem;
                padding-bottom: 10rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
            .css-1d391kg {
                padding-top: 3.5rem;
                padding-right: 1rem;
                padding-bottom: 3.5rem;
                padding-left: 1rem;
                }
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
        section[data-testid="stSidebar"] .css-1d391kg {{width: 14rem;}}
        """, unsafe_allow_html=True)

@st.experimental_singleton
def load_css(path):
    with open(path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.experimental_singleton
def load_bootstrap_stylesheet(path):
    with open(path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def init_styles():
    st.set_page_config(layout="wide", page_title="Census", page_icon="./public/favicon.ico")
    load_bootstrap_stylesheet("./styles/bootstrap.min.css")
    load_css("./styles/main.css")
    reduce_top_padding()

    with st.sidebar:
        st.markdown('<h1>pru-viz <span class="badge badge-secondary">Beta</span></h1>',
        unsafe_allow_html=True)
        st.markdown("### A simple web app to visualise GE15 and census data with maps!")       
        badge_columns = cycle(st.columns(3))
        with next(badge_columns): badge(type="github", name="hewliyang/pru-viz")
        with next(badge_columns): badge(type="twitter", name="hewliyang")

        st.markdown("## Data sources")
        st.markdown(link_card("https://github.com/Thevesh/analysis-election-msia", "Thevesh", "Election"), unsafe_allow_html=True)
        st.markdown(link_card("https://github.com/dosm-malaysia/census_parlimen_df-open", "Department of Statistics <br/> Malaysia", "Census"), unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('## About')
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://twitter.com/hewliyang">@hewliyang</a></h6>',
            unsafe_allow_html=True,
        )