from pymongo import MongoClient, errors
Domain='127.0.0.1'
port=27017

# client = MongoClient(host=[str(Domain)+":"+str(port)],
# 		serverSelectionTimeoutMS=3000,
# 		username='apurvi',
# 		password='1234')
connection=MongoClient("mongodb://apurvi:1234@127.0.0.1/db2")
db=connection.db2
val=db.movie.find_one()
db.movie.insert_one({'name':'apurvi'})
cursor=db.movie.find()
for r in cursor:
	print("row\n ",r)


    