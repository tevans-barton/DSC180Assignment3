import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def null_plot(df):
    to_plot = df.isnull().mean().plot(kind = 'bar')
    plt.title('Distribution of Missing Values')
    return

def age_distribution_plot(df):
    if 'subject_age' in df.columns:
        age_for_plot = [int(x) for x in df.subject_age if isinstance(x, str) and x.isnumeric()]
    else:
        age_for_plot = df.perceived_age
    age_plot = plt.hist(age_for_plot, bins = np.arange(16, 60))
    plt.title('Age Distribution')
    return

def post_stop_plot(df):
    binary_map = {'Y' : 1,
              'N' : 0}
    temp = df.copy()
    temp['arrested'] = temp.arrested.map(binary_map)
    temp['property_seized'] = temp.property_seized.map(binary_map)
    temp['contraband_found'] = temp.contraband_found.map(binary_map)
    temp['searched'] = temp.searched.map(binary_map)
    z_grouped = temp.groupby('subject_race'). agg({'searched' : np.mean, 'arrested' : np.mean,
                                     'property_seized' : np.mean, 'contraband_found' : np.mean,}
                                     ).loc[['Asian', 'Black/African American', 'Native American', 'Pacific Islander', 'White']]
    to_plot = z_grouped.plot(kind = 'bar', color = ['blue', 'red', 'green', 'orange'])
    plt.title('Post Stop Outcomes Plot by Race')
    return

def plot_light_dark(light_df, dark_df, year):
    to_plot = pd.DataFrame()
    dark_df_stops = dark_df[['subject_race', 'stop_id']].groupby('subject_race').agg('count') / len(dark_df)
    light_df_stops = light_df[['subject_race', 'stop_id']].groupby('subject_race').agg('count') / len(light_df)
    total_df = (light_df_stops).copy()
    total_df['dark_stops'] = dark_df_stops['stop_id']
    total_df = total_df.rename(mapper = {'stop_id' : 'light_stops'}, axis = 1)
    plotted = total_df.plot(kind = 'bar')
    p, l = plotted.get_legend_handles_labels()
    plotted.legend(p, l, loc='upper left')
    plt.title('Stop Distributions by Race in Light and Dark Environments for ' + str(year))
    return

# def plot_service_area_stop_rate(df, service_area):
#     assert(isinstance(service_area, str)), 'Service Area Must be String'
#     to_plot_series = df.loc[service_area]
#     plot = to_plot_series.plot(kind = 'bar')
#     plt.title('Race Distributions for Service Area: ' + str(service_area))
#     return
