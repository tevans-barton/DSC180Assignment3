import pandas as pd
import numpy as np 
import geopandas as gpd
import os
import json
import sys


def clean_2014_2017(df):
	#Decrease granularity of race to conform to 2018-2019 races
	race_mapping = {
		'A' : 'Asian',
		'B' : 'Black/African American',
		'C' : 'Asian', 
		'D' : 'Asian',
		'F' : 'Asian',
		'G' : 'Pacific Islander',
		'H' : 'Hispanic/Latino/a',
		'I' : 'Native American',
		'J' : 'Asian',
		'K' : 'Asian',
		'L' : 'Asian',
		'O' : 'Other',
		'P' : 'Pacific Islander',
		'S' : 'Pacific Islander',
		'U' : 'Pacific Islander',
		'V' : 'Asian',
		'W' : 'White',
		'Z' : 'Middle Eastern or South Asian',
		'X' : None
	}
	df['subject_race'] = df['subject_race'].map(race_mapping)
	#Map Sex to full word
	sex_mapping = {
		'M' : 'Male',
		'F' : 'Female',
		'X' : 'Other'
	}
	df['subject_sex'] = df['subject_sex'].map(sex_mapping)
	def fix_age(age):
		try:
			mod_age = int(age)
			if mod_age > 113:
				return np.nan
			else:
				return mod_age
		except ValueError:
			return np.nan

	df['subject_age'] = df['subject_age'].apply(lambda x: fix_age(x))
	#Map binary entries
	reg_binary_mapping = {
		'Y' : 'Y',
		'N' : 'N',
		'n' : 'N',
		'y' : 'Y',
		' ' : np.nan,
		'b' : np.nan,
		'M' : np.nan
	}
	def arr_search_convert(val):
		if isinstance(val, float) or val == 'N':
			return 'N'
		else:
			return 'Y'
	df['arrested'] = df['arrested'].apply(lambda x: arr_search_convert(x))
	df['searched'] = df['searched'].apply(lambda x: arr_search_convert(x))
	df['obtained_consent'] = df['obtained_consent'].map(reg_binary_mapping)
	df['contraband_found'] = df['contraband_found'].apply(lambda x: arr_search_convert(x))
	df['property_seized'] = df['property_seized'].apply(lambda x: arr_search_convert(x))
	return df



def clean_2018_2019(df):
    beats_and_serv_areas = gpd.read_file('../data/pd_beats_datasd/pd_beats_datasd.shp')
    beats_serv_dict = beats_and_serv_areas[['beat', 'serv']].set_index('beat', drop = True).serv.to_dict()
    df['stop_cause'] = df['reason_for_stop']
    df['subject_race'] = df['race']
    df['subject_age'] = df['perceived_age']
    df['service_area'] = df['beat'].map(beats_serv_dict)
    df = df.drop('beat', axis = 1)
    arrested_2018 = ['Y' if 'arrest' in x or 'Arrest' in x or 'hold' in x else 'N' for x in df.result]
    df['arrested'] = arrested_2018
    searched_2018 = ['N' if x is np.nan else 'Y' for x in df.basis_for_search]
    df['searched'] = searched_2018
    df['obtained_consent'] = df['consented']
    contraband_2018 = ['Y' if x != 'None' else 'N' for x in df.contraband]
    df['contraband_found'] = contraband_2018
    property_2018 = ['N' if x is np.nan else 'Y' for x in df.type_of_property_seized]
    df['property_seized'] = property_2018
    return df[['stop_id', 'stop_cause', 'service_area', 'subject_race', 'perceived_gender', 'subject_age', 
                'date_stop', 'time_stop', 'arrested', 'searched', 'obtained_consent', 'contraband_found',
                'property_seized']]











