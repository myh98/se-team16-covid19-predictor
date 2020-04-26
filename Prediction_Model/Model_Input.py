from pymongo import MongoClient, errors
from database import mongo_DB
import pandas as pd

db=mongo_DB()

def formcsv():
	
	db_values=db.entire_collection("zone_data")
	zones=[]
	new_values=[]
	death=[]
	date=[]
	# inputDF=pd.Dataframe()

	
	for x in db_values:
		zones.append(x['zone'])
		new_values.append(x['new'])
		death.append(x['death'])
		date.append(x['date'])
		
	inputDF=pd.DataFrame(date)
	inputDF.columns=["date"]
	inputDF["zone"]=zones
	inputDF["new"]=new_values
	inputDF["death"]=death 
	inputDF.to_csv("data_files/my_final_sample.csv",index=None)


if __name__ == '__main__':
	formcsv()

