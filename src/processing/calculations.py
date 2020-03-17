import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

def calc_total_stop_rates(cleaned_census, year_df):
    temp_stop_id = year_df[['stop_id', 'subject_race']].groupby('subject_race').agg('count')['stop_id']
    summed_census = cleaned_census.sum()
    to_return = temp_stop_id / summed_census
    to_return = to_return.dropna()
    if 'Other' in to_return.index:
        to_return = to_return.drop('Other')
    return to_return

def calc_stop_rates_by_service_area(cleaned_census, year_df):
    temp = cleaned_census[['White', 'Black/African American', 'Native American', 'Asian', 'Pacific Islander']]
    formatted_df = year_df.pivot_table(index = 'service_area', columns = 'subject_race', values = 'stop_id', aggfunc = 'count').fillna(0)
    formatted_df = formatted_df[['White', 'Black/African American', 'Native American', 'Asian', 'Pacific Islander']]
    return formatted_df.divide(temp).dropna(how = 'all')

def get_inner_twilight_period(df_passed):
    df = df_passed.copy()
    df = df.dropna(subset = ['time_stop']).reset_index(drop = True)
    df['time_stop'] = pd.to_datetime(df['time_stop'], errors = 'coerce')
    df = df.dropna(subset = ['time_stop']).reset_index(drop = True)
    start_twil_time = pd.to_datetime('17:09:00')
    end_twil_time = pd.to_datetime('20:29:00')
    def is_in_twil(datetime):
        if datetime.time() >= start_twil_time.time() and datetime.time() <= end_twil_time.time():
            return True
        else:
            return False
    df['is_in_twilight'] = df['time_stop'].apply(lambda x: is_in_twil(x))
    df = df[df['is_in_twilight']].reset_index(drop = True)
    return df

def veil_of_darkness(df_passed):
    df = df_passed.copy()
    sunsets = pd.read_csv('../data/monthwise_sunset.csv')[0:12]
    sunsets = sunsets.drop(['Day', 'Age of Moon', 'Rise', 'Culm'], axis = 1)
    sunsets = sunsets.set_index('Month', drop = True)
    sunsets['Set'] = pd.to_datetime(sunsets.Set)
    sunset_dict = sunsets['Set'].to_dict()
    df['Month'] = df['date_stop'].str.slice(5,7).astype(int)
    df['Sunset'] = df['Month'].map(sunset_dict)
    is_dark = df['time_stop'] > df['Sunset']
    df['Dark'] = is_dark
    return df

def calc_ks(light_df, dark_df):
    t1 = (dark_df[['stop_id', 'subject_race']].groupby('subject_race').agg('count') / len(dark_df))['stop_id']
    t2 = (light_df[['stop_id', 'subject_race']].groupby('subject_race').agg('count') / len(light_df))['stop_id']
    s1 = set(t1.index)
    s2 = set(t2.index)
    diff1 = list(s1 - s2)
    diff2 = list(s2 - s1)
    for e in diff1:
        t2[e] = 0
    for e in diff2:
        t1[e] = 0
    return scipy.stats.ks_2samp(t1.values, t2.values)
