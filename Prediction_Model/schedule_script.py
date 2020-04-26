
import schedule
import time
import os

def init_zone():
	# print("in func")
	os.system('python3 init_zoneDB.py')
	# os.system('ls -l')

schedule.every(1).minutes.do(init_zone)
while True:
	schedule.run_pending()
	time.sleep(5)
	# print("done with 5 min")
