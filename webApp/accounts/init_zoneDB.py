from pymongo import MongoClient, errors

connection=MongoClient("mongodb://apurvi:1234@127.0.0.1/db2")
db=connection.db2

zone_list=['z1','z2','z3','z4']

for z in zone_list:
	db_entry={'zone':z,'active':0,'recovered':0,'death':0,'empty_beds':0,'empty_ven':0,'ppe_stock':0}
	db.zone_data.insert_one(db_entry)

