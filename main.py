import streamlit as st
import pandas as pd
import re
import json
from itertools import cycle
from streamlit_echarts import st_echarts
from utils.maps import map_cont_echarts, map_results_echarts
from utils.cards import result_card
from streamlit_extras.colored_header import colored_header
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.badges import badge

geojson_url = "https://raw.githubusercontent.com/dosm-malaysia/data-open/main/datasets/geodata/electoral_0_parlimen.geojson"

@st.experimental_singleton
def load_css(path):
    with open(path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.experimental_singleton
def load_bootstrap_stylesheet(path):
    #return st.markdown(bootstrap_stylesheet, unsafe_allow_html=True)
    with open(path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.experimental_memo
def load_data():
    results = pd.read_csv("./data/results_parlimen_ge15.csv")
    geojson = json.load(open("./geo/parlimen_adjusted.geojson"))
    candidates = pd.read_csv("./data/candidates_ge15.csv")

    # split party names into the full name ; alias

    # regex helper
    def split(party: str):
        r = re.split(r"\((.*?)\)", party)
        return r[0], r[1]
    
    candidates = candidates.assign(
        party_short = lambda df_: df_["party"].map(lambda x: split(x)[1]),
        party = lambda df_: df_["party"].map(lambda x: split(x)[0])
    )

    return results, geojson, candidates

def main():
    st.title("pru-viz")
    badge_columns = cycle(st.columns(17))
    with next(badge_columns): badge(type="github", name="hewliyang/pru-viz")
    with next(badge_columns): badge(type="twitter", name="hewliyang")

    # read in data
    results, geojson, candidates = load_data()  

    # do a log transformation on the pengundi_jumlah column - need to refactor this
    # results["log_total"] = np.log(results["pengundi_jumlah"])

    options = ["Results", "Registered Voters"]
    index = 0



    selected_map = st.selectbox(label="Select metric:",options=options, index=index)
    # display log transform option if selected ~results
    if selected_map != "Results":
        log_flag = st.checkbox("Log Transform")

    col1, col2 = st.columns((3,1))
    with col1:
        colored_header(
            label = "Interactive Map",
            description = "Click on the legends, they are interactive!. Click on a region to display the corresponding breakdown!",
            color_name = "light-blue-70"
        )
        if selected_map == options[0]:
            map, options = map_results_echarts(candidate_df=candidates, geojson=geojson)
            clicked_state = st_echarts(options, map=map, height=800, key="result",
                events={"click": "function(params) {return params.name}"})
        elif selected_map == options[1]:
            target = "pengundi_jumlah"
            map, options = map_cont_echarts(result_df=results, geojson=geojson, target=target,
                title="GE15 Registered Voters by Parliament (2022)", log_flag=log_flag)
            clicked_state = st_echarts(options, map=map, height=800, key="voter",
                events={"click": "function(params) {return params.name}"})

    if clicked_state is None:
        return
    
    filtered_df = results[results.parlimen==clicked_state]
    filtered_candidates = candidates[candidates.parlimen==clicked_state].sort_values(by="votes", ascending=False)

    with col2:
        colored_header(
            label = "Results",
            description = "Personal information in the order: age, sex, race",
            color_name = "violet-70"
        )
        # st.dataframe(filtered_df)
        # st.dataframe(filtered_candidates)

        # display state + parlimen
        st.markdown(f"""##### **{filtered_df["state"].iloc[0]} - {filtered_df["parlimen"].iloc[0]}**""")

        # create and display result cards
        for _, row in filtered_candidates.iterrows():
            card = result_card(
                candidate_name = row["name_display"],
                party_name = row["party"]+f" ({row['party_short']})",
                vote_count = row["votes"],
                result = row["result"],
                result_desc = row["result_desc"],
                candidate_age = row["age"],
                candidate_sex = row["sex"],
                candidate_race = row["ethnicity"])
            st.markdown(card, unsafe_allow_html=True)

    # display the dataframe in an expander
    with st.expander("Explore the raw data!"):
        df_exp = dataframe_explorer(candidates)
        st.dataframe(df_exp, use_container_width=True)



if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="pru-viz", page_icon="./public/malaysia.ico")
    load_bootstrap_stylesheet("./styles/bootstrap.min.css")
    load_css("./styles/main.css")
    main()
