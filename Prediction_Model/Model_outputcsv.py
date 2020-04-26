from pymongo import MongoClient, errors
from database import mongo_DB
import pandas as pd

db=mongo_DB()

df=pd.read_csv("final_dataset.csv")
output_values=df.to_numpy()
print(output_values.shape)

for i in range(output_values.shape[0]):
	zone=output_values[i,16]
	predicted_risk=output_values[i,15]
	
	print(output_values[i,1])

