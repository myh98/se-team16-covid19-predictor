from pymongo import MongoClient, errors
from database import mongo_DB
import pandas as pd

db=mongo_DB()

df=pd.read_csv("final_dataset.csv")
output_values=df.to_numpy()
# print(output_values.shape)

for i in range(output_values.shape[0]):
	x_val=[] #predicted new cases
	y_val=[] #predicted death cases 
	zone=output_values[i,16]
	predicted_risk=output_values[i,15]
	for j in range(1,8):
		x_val.append(output_values[i,j])

	for j in range(8,15):
		y_val.append(output_values[i,j])

	db_entry={'zone':zone,'predicted_risk':predicted_risk,"1_x":x_val[0],"2_x":x_val[1],"3_x":x_val[2],"4_x":x_val[3],"5_x":x_val[4],"6_x":x_val[5],"7_x":x_val[6]
	,"1_y":y_val[0],"2_y":y_val[1],"3_y":y_val[2],"4_y":y_val[3],"5_y":y_val[4],"6_y":y_val[5],"7_y":y_val[6]} 
	db.insert("output_details",db_entry)

	# print(output_values[i,1])

