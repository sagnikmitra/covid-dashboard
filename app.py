import streamlit as st
import csv
import urllib.request
import pandas as pd
st.title('Covid Dashboard')
district_wise_url = "http://api.covid19india.org/csv/latest/cowin_vaccine_data_districtwise.csv"
vac_state_wise_url = "http://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv"
india_vac_url = "http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv"
selected = st.sidebar.selectbox("View Data by", ("Choose Below","District","State","Country","View All"))


if selected == "Choose Below":
    st.info("Choose any option from the Sidebar to access the data")


if selected =="District":
    st.info("This might take upto 30 seconds, as we are fetching the Data Realtime")
    url = district_wise_url
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    dist_data = []
    for row in cr:
        dist_data.append(row)
    dist_df = pd.DataFrame(dist_data)
    st.dataframe(dist_df)


if selected == "State":
    st.info("This might take upto 30 seconds, as we are fetching the Data Realtime")
    url = vac_state_wise_url
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    state_data = []
    for row in cr:
        state_data.append(row)
    state_df = pd.DataFrame(state_data)
    st.dataframe(state_df)


if selected == "Country":
    st.info("This might take upto 30 seconds, as we are fetching the Data Realtime")
    url = india_vac_url
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    india_data = []
    for row in cr:
        india_data.append(row)
    india_df = pd.DataFrame(india_data)
    st.dataframe(india_df)
    new_cols = ["updated_on", "state", "doses", "sessions",
            "sites", "first_dose", "second_dose", "male_doses", 
            "female_doses", "transgender_doses", "covaxin_doses", "covi_shield_doses", 
            "sputnik_v_doses", "aefi", "x18_44_doses", "x45_60_doses",     
            "x60_doses", "x18_44", "x45_60", "x60",              
            "male", "female", "transgender"]
    india_df.columns = new_cols
    india_df.drop(0)
    india_vac = india_df.loc[india_df['state']=='India']
    india_vac['date'] = pd.to_datetime(india_vac['updated_on'])
    india_vac['month'] = pd.DatetimeIndex(india_vac['date']).month
    india_vac = india_vac[['date', 'month', 'state', 'doses', 'sessions',
                       'sites', 'first_dose', 'second_dose', 'male', 'female',
                       'transgender', 'x18_44', 'x45_60', 'x60', 'covaxin_doses',
                       'covi_shield_doses', 'sputnik_v_doses', 'aefi']]
    india_vac = india_vac.rename(columns={'first_dose': 'dose1', 
                          'second_dose':'dose2',
                          'x18_44':'age18_45',
                          'x45_60':'age45_60',
                          'x60': 'age60plus',
                          'covaxin_doses':'covaxin',
                          'covi_shield_doses': 'covishield',
                          'sputnik_v_doses':'sputnikv'})
    cols = list(india_vac.columns)
    cols = cols[3:]
    for i in cols:
        india_vac[i] = pd.to_numeric(india_vac[i])
    tar_col = ['doses', 'dose1', 'dose2', 'covaxin', 'covishield']
    for i in tar_col:
        india_vac['daily_'+i] = india_vac.groupby(['state'])[i].shift(1)
        india_vac['daily_'+i][1] = 0
        india_vac['daily_'+i] = india_vac[i]-india_vac['daily_'+i]
    india_vac['daily_pct_dose1'] = round(india_vac['daily_dose1']/india_vac['daily_doses']*100, 2)

    india_vac['daily_pct_dose2'] = round(india_vac['daily_dose2']/india_vac['daily_doses']*100, 2)
    india_vac_pos = india_vac.loc[india_vac['daily_doses']>0]
    chart_data = pd.DataFrame(india_vac_pos,columns=[ 'daily_doses','daily_covaxin'])
    
    st.line_chart(chart_data)
    last_ind = len(india_vac_pos)
    dose_rate = (india_vac_pos['doses'][last_ind] - india_vac_pos['doses'][last_ind-1])*100/india_vac_pos['daily_doses'][last_ind-1]
    vaxin_rate = (india_vac_pos['daily_dose1'][last_ind] - india_vac_pos['daily_dose1'][last_ind-1])*100/india_vac_pos['daily_dose1'][last_ind-1]
    shield_rate = (india_vac_pos['daily_dose2'][last_ind] - india_vac_pos['daily_dose2'][last_ind-1]*100)/india_vac_pos['daily_dose2'][last_ind-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("Daily Doses", india_vac_pos['daily_doses'][last_ind],str(round(dose_rate,2))+'%' )
    col2.metric("Daily dose2",india_vac_pos['daily_covishield'][last_ind], str(round(shield_rate,2))+'%')
    col3.metric("Daily dose1",india_vac_pos['daily_covaxin'][last_ind], str(round(vaxin_rate,2))+'%')


if selected == "View All":
    st.info("This might take upto 30 seconds, as we are fetching the Data Realtime")
    url = district_wise_url
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    dist_data = []
    for row in cr:
        dist_data.append(row)
    dist_df = pd.DataFrame(dist_data)
    url = vac_state_wise_url
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    state_data = []
    for row in cr:
        state_data.append(row)
    state_df = pd.DataFrame(state_data)
    url = india_vac_url
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    india_data = []
    for row in cr:
        india_data.append(row)
    india_df = pd.DataFrame(india_data)
    st.dataframe(dist_df)
    st.dataframe(state_df)
    st.dataframe(india_df)
