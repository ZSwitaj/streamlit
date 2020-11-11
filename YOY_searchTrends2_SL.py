import pandas as pd
from pytrends.request import TrendReq
import streamlit as st
from datetime import date


def getTrendData(keyword):

    """

    Parameters
    ----------
    keyword : str
        Keyword to get trend data for

    Returns
    -------
    yoyIncrease : float
        Year-over-year increase for given keyword

    """

    dataset= []
    
    #Start date of last year's time frame
    start_date = st.sidebar.date_input(
        "Start of last year's time frame",
        value = date(2020,9,1),
        key = 'start date')
    
    #End date of this year's time frame
#    end_date = st.sidebar.date_input(
 #       "End of this year's time frame",
  #       value = date(2020,9,26),
   #      key = 'end date')
    
    end_date = date(2020,9,26)
    
    timeFrame = start_date.strftime('%Y-%m-%d')+' ' + end_date.strftime("%Y-%m-%d")
    
    pytrends = TrendReq(hl='en-US', tz=360) #Create pytrend query
    
    pytrends.build_payload(kw_list = [keyword],      # Build payload
                            timeframe = timeFrame,   # Timeframe from above
                            geo = 'US')              # US only, remove for global
    data = pytrends.interest_over_time()             # Pull data from query
    if not data.empty:
        data = data.drop(labels = ['isPartial'], axis ='columns')
        dataset.append(data)                         # Cleaning df
            
    dataset = pd.concat(dataset, axis = 1)
    
    lastYear = dataset.head(4)                      #Last year's data is first four weeks of df
    thisYear = dataset.tail(4)                      #This year's data is last four weeks of df
    
    df = pd.DataFrame()
    df = df.append(lastYear)
    df = df.append(thisYear)

    yoyIncrease = ((thisYear.mean(axis=0)[0] - lastYear.mean(axis=0)[0]) / lastYear.mean(axis=0)[0]) * 100

    return yoyIncrease

def getSuggestions(keyword):
    
    """
    Parameters:
    Keyword (str): Keyword to look for suggestions for
    
    Returns:
    df: Dateframe of suggestions, where mid is keyword ID for associated type
    """
    
    pytrends = TrendReq(hl='en-US', tz=360)
    
    suggestions = (pytrends.suggestions(keyword))
    suggestions = pd.DataFrame(suggestions)
    
    return suggestions

kw_dict = {
    "Timberland": "/m/05kv16",
    "Timberland Boots": "Timberland Boots",
    "UGG": "/m/06wccjq"
    # "Dr Martens": "/m/01lsm6",
    # "Merrell": "/m/0kqrz3",
    # "The North Face": "/m/04n92b",
    # "Patagonia": "/m/0g152j",
    # "Allbirds": "/g/11g6j4k3hl",
    # "Vans": "/m/04kbwy",
    # "Amazon": "/m/0mgkg ",
    # "Walmart": "/m/0841v",
    # "Target": "/m/01b39j",
    # "Zappos": "/m/02dfb9",
    # "Foot Locker": "/m/08fhy9",
    # "Journeys": "/m/03cbgd",
    # "DSW": "/m/0flp70",
    # "Nordstrom": "/m/01fc_q",
    # "Macy's": "/m/01pkxd ",
    # "REI": "/m/02nx4d",
    # "Dick's Sports": "/m/06fgv_",
    # "Boot": "/m/01b638",
    # "Outerwear": "Outerwear"
    }

lst_keywords = []

print("Adding keywords...")
for topic in kw_dict:
    lst_keywords.append(topic)

lst_values = []

for topic in kw_dict:
    print("Calculting {} results".format(topic))
    lst_values.append(round(getTrendData(kw_dict[topic]),1))

print("Combining...")
res = dict(zip(lst_keywords, lst_values))
res_df = pd.DataFrame.from_dict(res, orient = 'index', columns = ['YOY Change'])
res_df = res_df.transpose()

st.subheader('Raw data')
st.write(res_df)
