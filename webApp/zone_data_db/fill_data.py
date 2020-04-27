from pymongo import MongoClient, errors
from database_func import mongo_DB
import pandas as pd

db=mongo_DB()

# db.drop_collection("output_details")
df=pd.read_csv("db_data.csv")
val=df.to_numpy()
# print(output_values.shape)
# print(df.shape)
for i in range(val.shape[0]):
	date = val[i,0]
	# print(date)
	empty_beds = val[i,1]
	recovered = val[i,2]
	death = val[i,3]
	active = val[i,4]
	empty_ven = val[i,5]
	new = val[i,6]
	ppe_stock = val[i,7]
	zone = val[i,8]
	db_entry={'zone':zone,'date':date,'empty_beds':empty_beds,'recovered':recovered,'death':death,'active':active,'empty_ven':empty_ven,'new':new,'ppe_stock':ppe_stock} 
	db.insert("zone_data",db_entry)
	# print(output_values[i,1])

