
import schedule
import time
import os


def generate_csv():
	print("in func generate_csv")
	# os.system('pkill -f "python3 manage.py runserver"')
	os.system('python3 heatmap_csv.py')

def generate_heatmap():
	print("in func generate_heatmap")
	os.system('python3 heatmap.py')
	# time.sleep(10)

def initialize_zone_db():
	print("in func initialize_zone_db")
	# os.system('python3 /accounts/init_zoneDB.py')
	# os.system('python3 manage.py runserver 0.0.0.0:8000')

# def run_web():
# 	print("in func run_web")
# 	os.system('python3 manage.py runserver 0.0.0.0:8000')

# def init_zone():
# 	# print("in func")
# 	os.system('python3 init_zoneDB.py')
# 	# os.system('ls -l')

# schedule.every(1).minutes.do(init_zone)

# schedule.every().day.at("07:55").do(run_web)
schedule.every().day.at("08:16").do(generate_csv) 
schedule.every().day.at("08:18").do(generate_heatmap) 
schedule.every().day.at("08:20").do(initialize_zone_db) 
while True:
	schedule.run_pending()
	time.sleep(5)
	# print("done with 5 min")

