import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

def light_or_dark(df_passed):
    df = df_passed.copy()
    r = requests.get('https://api.sunrise-sunset.org/json', params={'lat': 32, 'lng': -117}).json()['results']

