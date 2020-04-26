from pymongo import MongoClient, errors
from database_func import mongo_DB
import pandas as pd

db=mongo_DB()

def formcsv():
	
	db_values=db.entire_collection("output_details")
	zones=[]
	x_1=[]
	x_2=[]
	x_3=[]
	x_4=[]
	x_5=[]
	x_6=[]
	x_7=[]
	y_1=[]
	y_2=[]
	y_3=[]
	y_4=[]
	y_5=[]
	y_6=[]
	y_7=[]
	predicted_risks=[]
	# inputDF=pd.Dataframe()

	
	for x in db_values:
		zones.append(x['zone'])
		x_1.append(x['1_x'])
		x_2.append(x['2_x'])
		x_3.append(x['3_x'])
		x_4.append(x['4_x'])
		x_5.append(x['5_x'])
		x_6.append(x['6_x'])
		x_7.append(x['7_x'])

		y_1.append(x['1_y'])
		y_2.append(x['2_y'])
		y_3.append(x['3_y'])
		y_4.append(x['4_y'])
		y_5.append(x['5_y'])
		y_6.append(x['6_y'])
		y_7.append(x['7_y'])
		predicted_risks.append(x['predicted_risk'])
		
	inputDF=pd.DataFrame(x_1)
	inputDF.columns=["1_x"]
	inputDF["2_x"]=x_2
	inputDF["3_x"]=x_3
	inputDF["4_x"]=x_4
	inputDF["5_x"]=x_5
	inputDF["6_x"]=x_6
	inputDF["7_x"]=x_7

	inputDF["1_y"]=y_1
	inputDF["2_y"]=y_2
	inputDF["3_y"]=y_3
	inputDF["4_y"]=y_4
	inputDF["5_y"]=y_5
	inputDF["6_y"]=y_6
	inputDF["7_y"]=y_7


	inputDF["predicted_risks"]=predicted_risks
	inputDF["location"]=zones
	inputDF.to_csv("final_dataset.csv",index=None)


if __name__ == '__main__':
	formcsv()

