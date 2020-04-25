from pymongo import MongoClient, errors
import datetime

connection=MongoClient("mongodb://hospit:1234@127.0.0.1/hospit_db")
db=connection.hospit_db

zone_list=['Alwal','Amberpet','Begumpet','Chandanagar','Chandrayangutta','Charminar','Falakunuma','Gajula Ramaram'
,'Goshamahal','Hayathnagar','Jubilee Hills','Kapra','Karwan','Khairatabad','Kukatpally','LB Nagar','Malakpet','Malkajgiri','Mehdipatnam','Moosapet','Musheerabad','Quthbullapur','Rajendra Nagar','Ramachandra Puram / Patancheru','Santhoshnagar','Saroornagar','Secunderabad Division','Serilingampally','Uppal','Yousufguda']

Current_Date = datetime.datetime.today()
Current_Date = str(Current_Date)
Current_Date = Current_Date.split(" ")[0]
li = Current_Date.split("-")
li.reverse()
curr_date = "/".join(li)
# print(curr_date)

for z in zone_list:
	# print(z)
	db_entry={'zone':z,'date':curr_date, 'new':0, 'active':0,'recovered':0,'death':0,'empty_beds':0,'empty_ven':0,'ppe_stock':0}
	db.zone_data.insert_one(db_entry)

	
