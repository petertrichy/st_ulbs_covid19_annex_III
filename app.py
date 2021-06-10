import pandas as pd
from pathlib import Path
import sqlite3
from sqlite3 import Connection
import streamlit as st
import csv

URI_SQLITE_DB = "covid19_annex_iii.db"

def main():
    st.title("My Database")
    st.markdown("Enter data in database from sidebar, then click 'Save to database'")

    # read ulbs name from ulbs.csv
    ulbs = pd.read_csv("ulb_list.csv")

    conn = get_connection(URI_SQLITE_DB)
    init_db(conn)

    build_sidebar(conn, ulbs)
    display_data(conn)


def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS covid19_annex_iii
            (
                ULB_NAME VARCHAR2(30),
                SAMPLES_TESTED_TODAY INT,
                POSITIVE_TODAY INT,
                POSITIVE_RATE FLOAT,
                IN_HOME_QUARANTINE INT,
                IN_COVID_CARE_CENTRE INT,
                IN_HOSPITAL INT,
                COVID_CARE_CENTRES INT,
                CONTAINMENT_ZONES INT,
                VEGETABLE_VEHICLES INT
            );"""
    )
    conn.commit()

def build_sidebar(conn: Connection, ulbs):
    st.header("COVID19 ANNEXURE-III DETAILS")
    ulb = st.selectbox(
        "Name of the ULB",
        ulbs)
    sample_tested_today = int(st.text_input("Samples tested today", 0, 1000))
    positive_today = int(st.text_input("Positive today", 0, 1000))
    in_home_quarantine = st.text_input("In Home Quarantine", 0, 1000)
    in_covid_care_centre = st.text_input("In Covid Care Centre", 0, 1000)
    in_hospital = st.text_input("In Hospital", 0, 1000)
    covid_care_centres = st.text_input("Covid Care Centres", 0, 1000)
    containment_zones = st.text_input("Containment Zones", 0, 1000)
    vegetable_vehicles = st.text_input("Vegetable Vehicles", 0, 100)
    if st.button("Save to database"):
        positive_rate_today = positive_today / sample_tested_today * 100.0
        conn.execute(f"INSERT INTO covid19_annex_iii (ULB_NAME, SAMPLES_TESTED_TODAY, POSITIVE_TODAY, POSITIVE_RATE, IN_HOME_QUARANTINE, IN_COVID_CARE_CENTRE, CONTAINMENT_ZONES, VEGETABLE_VEHICLES) VALUES ('{ulb}', {sample_tested_today}, {positive_today}, {positive_rate_today}, {in_home_quarantine}, {in_covid_care_centre}, {in_hospital}, {covid_care_centres}, {containment_zones}, {vegetable_vehicles})")
        conn.commit()

def display_data(conn: Connection):
    if st.checkbox("Display data in sqlite database"):
        st.dataframe(get_data(conn))

def get_data(conn: Connection):
    df = pd.read_sql("SELECT * FROM test", con=conn)
    return df

@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit
    NB: https://stackoverflow.com/questions/48218065/programmingerro-sqlite-object
    """
    return sqlite3.connect(path, check_same_thread=False)

if __name__ == "__main__":
    main()
