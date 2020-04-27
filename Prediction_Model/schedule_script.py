
import schedule
import time
import os


def model_input():
	print("in func model_input")
	os.system('python3 Model_Input.py')

def get_predictions():
	print("in func get_predictions")
	os.system('conda activate work')
	os.system('python3 get_predictions.py')
	os.system('conda activate work')
	# time.sleep(10)

def model_output():
	print("in func model_output")
	os.system('python3 Model_output.py')

# def init_zone():
# 	# print("in func")
# 	os.system('python3 init_zoneDB.py')
# 	# os.system('ls -l')

# schedule.every(1).minutes.do(init_zone)
schedule.every().day.at("07:10").do(model_input) 
schedule.every().day.at("07:12").do(get_predictions) 
schedule.every().day.at("07:15").do(model_output) 
while True:
	schedule.run_pending()
	time.sleep(5)
	# print("done with 5 min")
