import schedule
import time
import datetime
import threading
from googlemaps import Client
from time import gmtime, strftime

def partial(func, *args, **kwargs):
	def f(*args_rest, **kwargs_rest):
		kw = kwargs.copy()
		kw.update(kwargs_rest)
		return func(*(args + args_rest), **kw) 
	return f

def format_time(hours, minutes):
	return str(hours)+":"+str(minutes)+"0"

def find_traffic(hours, minutes):
	addresses = []
	gmaps = Client('AIzaSyCaQlauoQ1njrABzhVCliY49DaByZNYkTY')
	cassie_work = '3237 S 16th St, Milwaukee, WI 53215'
	joey_work = '1550 Innovation Way, Hartford, WI 53027'
	with open('address.txt') as f:
		addresses = f.readlines()
	file = open('times.csv', 'a')
	day = datetime.datetime.today().weekday()
	for addr_newline in addresses:
		addr = addr_newline.rstrip()
		directions_cassie = None
		directions_joey = None
		if(hours < 8):
			directions_cassie = gmaps.directions(addr, cassie_work)
			directions_joey = gmaps.directions(addr, joey_work)
		else:
			directions_cassie = gmaps.directions(cassie_work, addr)
			directions_joey = gmaps.directions(joey_work, addr)
		file.write(str(addr)+','+format_time(hours,minutes)+',Cassie,'+str(directions_cassie[0]['legs'][0]['duration']['value'])+',Joey,'+str(directions_joey[0]['legs'][0]['duration']['value'])+','+day+'\n')
	file.close()

def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()

def test_job():
	print("TEST TEST TEST")

def upload_file():
	times = []
	with open('times.csv') as f:
		times = f.readlines()
	for time in times:
		time = time.rstrip()
		time = time.split(',')
		data = {'address':time[0]+time[1]+time[2], 'time':time[3], 'Cassie':time[5], 'Joey':time[7]}
		r = requests.post('localhost:8000', data=data)

def schedule_tasks():
	hours = 5
	minutes = 0
	for y in range(0,6):
		for x in range(0,6):
			p = partial(find_traffic, hours, minutes)
			schedule.every().day.at(format_time(hours, minutes)).do(p)
			minutes += 1
		minutes = 0
		if(y == 2):
			hours += 7
		else:
			hours += 1
	#schedule.every().day.at('9:00').do(upload_file())
	#schedule.every().day.at('18:00').do(upload_file())

def schedule_tasks_test():
	hours = 22
	minutes = 3
	for y in range(0,2):
		for x in range(0,1):
			p = partial(find_traffic, hours, minutes)
			schedule.every().day.at(format_time(hours, minutes)).do(p)
			minutes += 1
		minutes = 0
		hours += 1
	#schedule.every().day.at('22:03').do(run_threaded,test_job)

#schedule_tasks()
#schedule_tasks_test()
#find_traffic(5, 69)
upload_file()
while True:
	schedule.run_pending()
	time.sleep(30)
