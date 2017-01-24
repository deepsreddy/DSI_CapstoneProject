import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np
import random
import scipy.stats as ss
from scipy.stats import norm
from textblob import TextBlob
import sexmachine.detector as gender
    
def read_businessdata(cityname):
	filename = 'data_full/' + cityname + '_Restaurants.json'
	rest_df = pd.read_json(filename)
	return rest_df

def read_userdata(cityname):
	filename = 'data_full/' + cityname + '_UserData.json'
	user_df = pd.read_json(filename)
	return user_df

def read_reviewdata(cityname):
	filename = 'data_full/' + cityname + '_ReviewData.json'
	review_df = pd.read_json(filename)
	return review_df

def read_tipdata(cityname):
	filename = 'data_full/' + cityname + '_TipData.json'
	tip_df =  pd.read_json(filename)
	return tip_df

#extract feature#1 (longitude of restaurant)
def extract_feature1(city_df):
	latitude = city_df['latitude']
	return latitude

#extract feature#2 (longitude of restaurant)
def extract_feature2(city_df):
	longitude = city_df['longitude']
	return longitude

#extract feature#3 (zipcode of restaurant)
def extract_feature3(city_df):
	zipcodes= []
	address = city_df['full_address']
	for entry in address:
		entries = entry.split(" ")
		zipcode = entries[-1]
		if(zipcode.isdigit()):
			zipcodes.append(int(zipcode))
		else:
			zipcodes.append(zipcodes[-1])
	return zipcodes

#extract feature#4 (population density based on zipcode)
def extract_feature4(zipcodes):
	pop_densities = []
	unique_zipcodes = list(set(zipcodes))
	pop_density_df = pd.read_excel('data_full/Zipcode-ZCTA-Population-Density-And-Area-Unsorted.xlsx', converters={'Zip/ZCTA': str})

	for each_zipcode in unique_zipcodes:
		idx = pop_density_df[pop_density_df['Zip/ZCTA'] == str(each_zipcode)].index.tolist()
	if idx:
		pop_densities.append(pop_density_df['Density Per Sq Mile'][idx[0]])
	else:
		pop_densities.append('NA')
    
	return pop_densities

#extract feature#5 (review_count)
def extract_feature5(city_df):
	review_count = city_df['review_count']
	return review_count

#extract feature#6 (gender from user's first name)
def extract_feature6(rest_df, user_df, review_df):
	male_female_ratios = []
	#df_grp_business = review_df.groupby(review_df.business_id).count()	            
	#businesses = df_grp_business.index
	businesses = rest_df['business_id']
	index = 0
	for businessid in businesses:
		df_point = review_df[review_df['business_id'] == businessid]
		userlist = df_point['user_id']
		count_males = 0
		count_females = 0
		print(len(userlist))
		for eachuser in userlist:
			df_user = user_df[user_df['user_id'] == eachuser]
			username = df_user['name']
			mapped_name = map_gender(username)
			if(mapped_name == 'male'):
				count_males = count_males + 1
			if(mapped_name == 'female'):
				count_females = count_females + 1		
		if(count_females != 0):
			ratio = (count_males/count_females)
		else:
			ratio = 1.0
		male_female_ratios.append(ratio)
		print(len(userlist), index)
		index = index + 1
	return 	male_female_ratios
	
def map_gender(name):
	d = gender.Detector(case_sensitive=False)
	mapped_name = d.get_gender(str(name), 'usa')
	if(mapped_name == 'mostly_male'):
		mapped_name = 'male'
	elif(mapped_name == 'mostly_female'):
		mapped_name = 'female'
	elif(mapped_name == 'andy'):
		irand = random.randint(0,1)
		if(irand):
			mapped_name = 'male'
		else:
			mapped_name = 'female'
	return mapped_name


def extract_feature7_8_9(rest_df, user_df, review_df):
	avg_friendslist = []
	avg_fanslist = []
	avg_eliteyearslist = []
	businesses = rest_df['business_id']
	#df_grp_business = review_df.groupby(review_df.business_id).count()	            
	#businesses = df_grp_business.index
	index = 0
	for businessid in businesses:
		df_point = review_df[review_df['business_id'] == businessid]
		userlist = df_point['user_id']
		sum_fans = 0
		sum_friends = 0
		sum_elite = 0
		for eachuser in userlist:
			df_user = user_df[user_df['user_id'] == eachuser]
			fanlist = df_user['fans']
			friends = df_user['friends']
			eliteyears = df_user['elite']
			sum_fans = sum_fans + fanlist
			sum_friends = sum_friends + len(friends)
			sum_elite = sum_elite + len(eliteyears)
		if(len(userlist) > 0):
			avg_fans = sum_fans/len(userlist)
			avg_friends = sum_friends/len(userlist)
			avg_elite = sum_elite/len(userlist)
		else:
			avg_fans = 0
			avg_friends = 0
			avg_elite = 0
		avg_friendslist.append(avg_friends)
		avg_fanslist.append(avg_fans)
		avg_eliteyearslist.append(avg_elite)
		if(index%100 == 0):
			print(index)
		index = index + 1
	return 	avg_friendslist, avg_fanlist, avg_elite


def extract_feature10_11_12(rest_df, user_df, review_df):
	avg_starslist = []
	std_starslist = []
	skew_starslist = []
	businesses = rest_df['business_id']
	#df_grp_business = review_df.groupby(review_df.business_id).count()	            
	#businesses = df_grp_business.index
	for businessid in businesses:
		df_point = review_df[review_df['business_id'] == businessid]
		userlist = df_point['user_id']
		sum_avgstars = 0
		for eachuser in userlist:
			df_user = user_df[user_df['user_id'] == eachuser]
			avgstars = df_user['average_stars']
			sum_avgstars = sum_avgstars + avgstars
		
	return 	avg_friendslist, avg_fanlist




