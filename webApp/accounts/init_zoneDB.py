from pymongo import MongoClient, errors

connection=MongoClient("mongodb://hospit:1234@127.0.0.1/hospit_db")
db=connection.hospit_db

zone_list=['Alwal','Amberpet','Begumpet','Chandanagar','Chandrayangutta','Charminar','Falakunuma','Gajula Ramaram'
,'Goshamahal','Hayathnagar','Jubilee Hills','Kapra','Karwan','Khairatabad','Kukatpally','LB Nagar','Malakpet','Malkajgiri','Mehdipatnam','Moosapet','Musheerabad','Quthbullapur','Rajendra Nagar','Ramachandra Puram / Patancheru','Santhoshnagar','Saroornagar','Secunderabad Division','Serilingampally','Uppal','Yousufguda']
for z in zone_list:
	db_entry={'zone':z,'active':0,'recovered':0,'death':0,'empty_beds':0,'empty_ven':0,'ppe_stock':0}
	db.zone_data.insert_one(db_entry)

	