import pandas as pd
from pytrends.request import TrendReq
from datetime import timedelta, date
import streamlit as st

overlap_days = 60

this_start_date = st.sidebar.date_input("This year's start date", date(2020,9,27))
this_end_date = st.sidebar.date_input("This year's end date", date(2020,10,24))
last_start_date = st.sidebar.date_input("Last year's start date", date(2019,9,29))
last_end_date = st.sidebar.date_input("last year's end date", date(2019,10,26))

timeRange = (this_end_date - this_start_date).days + 1
overlapDay = this_start_date - timedelta((((this_start_date - last_end_date)/2).days))
corrStartDate = overlapDay - timedelta(overlap_days/2)
corrEndDate = overlapDay + timedelta(overlap_days/2)

def getTrendData(keyword, start_date, end_date):
    
    pytrends = TrendReq(hl='en-US', tz=360)
    dataset = []

    timeFrame = start_date.strftime('%Y-%m-%d')+' ' + end_date.strftime("%Y-%m-%d")
    
    pytrends.build_payload(kw_list = [keyword],
                        timeframe = timeFrame,
                        geo = 'US')
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels = ['isPartial'], axis ='columns')
        dataset.append(data)
            
    dataset = pd.concat(dataset, axis = 1)
    
    return dataset

def getCorrFactors(lastYearData, thisYearData):

    correctionFactors = []
    i = 0
    lastYearTail = pd.DataFrame(lastYearData.tail(overlap_days + 1))
    thisYearHead = pd.DataFrame(thisYearData.head(overlap_days + 1))
    for i in range(len(lastYearTail)):
        correctionFactors.append((lastYearTail.iloc[i][0]/thisYearHead.iloc[i][0]))
        i += 1
        
    return sum(correctionFactors)/len(correctionFactors)

def correctDailyData(data, correctionFactor):
    return data / correctionFactor

def calcYOY(keyword, this_start_date = this_start_date, this_end_date = this_end_date, 
            last_start_date = last_start_date, last_end_date= last_end_date,
            corrStartDate = corrStartDate, corrEndDate = corrEndDate):
    
    thisYearPlus = getTrendData(keyword, corrStartDate, this_end_date)
    lastYearPlus = getTrendData(keyword, last_start_date, corrEndDate)
    corr = getCorrFactors(lastYearPlus, thisYearPlus)
    
    lastYearCorr = correctDailyData(lastYearPlus, corr)
    
    thisYearAns = thisYearPlus.tail(timeRange).mean(axis=0)[0]
    lastYearAns = lastYearCorr.head(timeRange).mean(axis=0)[0]
    
   # print(thisYearPlus.tail(timeRange).mean(axis=0)[0])
   # print(lastYearCorr.head(timeRange).mean(axis=0)[0])

    yoyIncrease = ((thisYearAns - lastYearAns)/ lastYearAns) * 100
    
    return str(round(yoyIncrease, 1)) + "%"
    
kw_dict = {
    "Timberland": "/m/05kv16",
    "Timberland Boots": "Timberland Boots",
    # "UGG": "/m/06wccjq",
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
    # "Outerwear": "Outerwear",
    # "Sneakers":"/m/09kjlm",
    # "Boat Shoes":"/m/05q55b9",
    # "Sandals":"/m/03nfch",
    # "Hiking":"/m/012v4j",
    # "Sustainability":"/m/0hkst",
    # "Back to school":"Back to school",
    # "Jimmy Choo":"/m/0hkst",
    # "Timberland PRO":"Timberland PRO",
    # "Red Wing":"/m/0603n6",
    # "Carhartt":"/m/08vntw",
    # "Wolverine":"/m/06ddr7",
    # "Dickies":"/m/03pjr5",
    # "Duluth":"/g/11f30mhkr2",
    # "Lowe's":"/m/037922",
    # "Home Depot":"/m/01zj1t",
    # "Grainger":"/m/0cp307",
    # # "Bobs":"Bobs",
    # "Boot Barn":"/g/11byc_x_1d",
    # "Work Boots":"Work Boots",
    # "Steel Toe Boots":"/m/01x101",
    # "Timberland Powertrain":"Timberland Powertrain",
    # "Safety Toe":"Safety Toe",
    # "Workwear":"/m/026lc7w",
    # "Nurse shoes":"Nurse shoes",
    # "Healthcare Discount":"Healthcare Discount",
    # "Responders Discount":"Responders Discount",
    # "Trade School":"/m/030x63",
    # "Home Improvement":"/m/03n2_q",
    # "DIY":"/m/017rcq"
    }

lst_keywords = []

print("Adding keywords...")
for topic in kw_dict:
    lst_keywords.append(topic)


lst_values = []

print("Calculating...")
for topic in kw_dict:
    print(topic)
    lst_values.append(calcYOY(kw_dict[topic]))

print("Combining...")
res = dict(zip(lst_keywords, lst_values))
res_df = pd.DataFrame.from_dict(res, orient = 'index', columns = ['YOY Change'])
res_df = res_df.transpose()

st.title('Google Trends Data')
st.write(res)
