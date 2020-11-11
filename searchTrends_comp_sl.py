import pandas as pd
import time
from pytrends.request import TrendReq
import streamlit as st
from datetime import datetime
startTime = time.time()

pytrend = TrendReq(hl = 'en-US', tz = 360)

colnames = ["keywords"]

df2 = st.sidebar.multiselect(
    'Choose which companies to include',
    ['Allbirds', 'TNF','Timberland Boots','UGG','Dr Martens', 'Merrell',
     'Patagonia', 'Allbirds','Vans','Jimmy Choo'])

begin_date = st.sidebar.date_input(
    'Enter start date',
    value = datetime(2020,1,1),)

end_date = st.sidebar.date_input(
    'Enter end date',
    value = datetime(2020,6,1),)

searchDates = begin_date.strftime('%Y-%m-%d')+' '+end_date.strftime('%Y-%m-%d')

dataset = []

@st.cache
def interest_over_time():
    for x in range(0, len(df2)):
        keywords = [df2[x]]
        pytrend.build_payload(kw_list = keywords,
                                timeframe = searchDates,
                                geo = 'US')
        data = pytrend.interest_over_time()
        if not data.empty:
            data = data.drop(labels = ['isPartial'], axis ='columns')
            dataset.append(data)
    return dataset
        
df = pd.concat(interest_over_time(), axis = 1)

"""
Streamlit Code
"""

st.title('Google Trends Competitor Data over Time')

if st.checkbox('Show raw data?'):
    st.subheader('Raw data')
    st.write(df)

st.line_chart(df)


