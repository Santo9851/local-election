from operator import index
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

province_no = st.selectbox('Please enter province number', options = ['1','2','3','4','5','6','7'])

province_url = 'https://result.election.gov.np/JSONFiles/Election2079/Local/VoteCountProvince'+province_no+'.json'

@st.cache
def scrapper(url):
    province = pd.read_json(url)
    province = pd.DataFrame(province)
    return province


data = scrapper(province_url)

district = data['DistrictName']
district.drop_duplicates(keep='first',inplace=True)
selected_district = st.selectbox('Please Select District', options=district)

district_for_process = data[data['DistrictName'] == selected_district]
local_level = district_for_process['LocalBodyName']
local_level.drop_duplicates(keep='first',inplace=True)
selected_local_level = st.selectbox('Please Select Local Level', options=local_level)

for_selecting_post = data[data['LocalBodyName'] == selected_local_level]
post = for_selecting_post['PostName']
post.drop_duplicates(keep='first',inplace=True)
selected_post = st.selectbox('Please Select Post' , options = post)

for_selecting_result = data[data['PostName'] == selected_post]
for_selecting_result = for_selecting_result[for_selecting_result['LocalBodyName'] == selected_local_level]
FinalResult = for_selecting_result.loc[:,['CandidateName', 'Age', 'WardNo', 'PoliticalPartyName', 'TotalVotesRecieved']]

dg = GridOptionsBuilder.from_dataframe(FinalResult)
AgGrid(FinalResult)
