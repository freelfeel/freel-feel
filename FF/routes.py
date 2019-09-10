import sqlite3,time,os
from datetime import datetime, timedelta
from flask import Flask, render_template, send_file, make_response, request, send_file
import pyowm

global owm  
owm= pyowm.OWM('b8ae5f3ca157ddb08c589e4922bf6930')
startTime = time.time()
app = Flask(__name__)

def getUptime():
	m, s = divmod(time.time() - startTime , 60)
	h, m = divmod(m, 60)
	return '{:02g}:{:02g}:{:.1f}'.format(h, m, s)	
	
	

# Helper Functions-----------------------------------------


#Retrieve local time
def local_time():
	ltime = format(datetime.now(), '%H:%M')
	return ltime	

# DATA RETRIEVAL Functions--------------------------------

#Retrieve last hour DATA
def last_hour():
	conn=sqlite3.connect('FFpir.db')
	curs=conn.cursor()
	for row in curs.execute("select count(*) from pir group by strftime('%Y-%m-%dT%H:00:00.000', timestamp) order by timestamp desc limit 1"):
		count = str(row[0])
		#conn.close()
	return count

#Retrieve last log DATA
def last_log():
	conn=sqlite3.connect('FFpir.db')
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM pir ORDER BY timestamp DESC LIMIT 1"):
		llog = str(row[0])
		#conn.close()
	return llog	

def last_day():
	conn=sqlite3.connect('FFpir.db')
	curs=conn.cursor()
	for row in curs.execute("select count(*) from pir group by strftime('%d', timestamp) order by timestamp desc limit 1"):
		count = str(row[0])
		#conn.close()
	return count	

def getFreelSpecific(year,month1,day1,hour1,month2,day2,hour2):
  conn=sqlite3.connect('FFpir.db')
  curs=conn.cursor()
  for row in curs.execute("SELECT strftime('%m',timestamp),strftime('%d',timestamp),strftime('%H',timestamp),count(*) FROM pir WHERE timestamp BETWEEN '"+year+"-"+month1+"-"+day1+" "+hour1+"' and '"+year+"-"+month2+"-"+day2+" "+hour2+"' group by strftime('%d %H',timestamp) order by strftime('%m %d %H',timestamp) desc"):
  	rows = curs.fetchall()
  	out = []
  	for row in rows:
  		out.append(row)
  return out	

def getFreelSpecificHOUR(year,month,day,hour1):
  conn=sqlite3.connect('FFpir.db')
  curs=conn.cursor()
  for row in curs.execute("SELECT count(*) FROM pir WHERE timestamp LIKE '"+year+"-"+month+"-"+day+" "+hour1+"%'"):
  	res = row[0]
  return res

def getFreelSpecificHOURS(year,month,day,hour1,hour2):
  conn=sqlite3.connect('FFpir.db')
  curs=conn.cursor()
  for row in curs.execute("SELECT count(*) FROM pir WHERE timestamp BETWEEN '"+year+"-"+month+"-"+day+" "+hour1+"' AND '"+year +"-"+month+"-"+day+" "+hour2+"'"):
  	res = row[0]
  return res

def getFreelSpecificDAY(year,month,day):
  conn=sqlite3.connect('FFpir.db')
  curs=conn.cursor()
  for row in curs.execute("SELECT count(*) FROM pir WHERE timestamp LIKE '"+year+"-"+month+"-"+day+"%'"):
  	res = row[0]
  return res    	

def getFreelSpecificDAYS(year,month,day1,day2):
  conn=sqlite3.connect('FFpir.db')
  curs=conn.cursor()
  for row in curs.execute("SELECT count(*) FROM pir WHERE timestamp BETWEEN '"+year+"-"+month+"-"+day1+"' AND '"+year +"-"+month+"-"+day2+"'"):
  	res = row[0]
  return res  

@app.route('/query_by_HOUR',methods = ['POST', 'GET'])
def query_by_HOUR():
	if request.method == 'POST':
		result = request.form
		resp = getFreelSpecificHOUR(result['year'],result['month'],result['day'],result['hour1'])
		lday = last_day()
		lhour = last_hour()
		llog = last_log()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'resp':resp,
		  'result':result,
		  'uptime':uptime,
		}
		return render_template("qbyHOUR.html",**templateData)	
	else:	      
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'uptime':uptime,
		}
		return render_template('qbyHOUR.html', **templateData)

@app.route('/query_by_DAY',methods = ['POST', 'GET'])
def query_by_DAY():
	if request.method == 'POST':
		result = request.form
		resp = getFreelSpecificDAY(result['year'],result['month'],result['day1'])
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'resp':resp,
		  'result':result,
		  'uptime':uptime,
		}
		return render_template("qbyDAY.html",**templateData)	
	else:	      
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'uptime':uptime,
		}
		return render_template('qbyDAY.html', **templateData)		

@app.route('/query_between_HOURS',methods = ['POST', 'GET'])
def query_between_HOURS():
	if request.method == 'POST':
		result = request.form
		resp = getFreelSpecificHOURS(result['year'],result['month'],result['day'],result['hour1'],result['hour2'])
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'resp':resp,
		  'result':result,
		  'uptime':uptime,
		}
		return render_template("qbetweenHOURS.html",**templateData)	
	else:	      
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'uptime':uptime,
		}
		return render_template('qbetweenHOURS.html', **templateData)

@app.route('/querySpecific',methods = ['POST', 'GET'])
def querySpecific():
	if request.method == 'POST':
		result = request.form
		resp = getFreelSpecific(result['year'],result['month1'],result['day1'],result['hour1'],result['month2'],result['day2'],result['hour2'])
		lhour = last_hour()
		lday = last_day()
		llog = last_log()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'resp':resp,
		  'result':result,
		  'uptime':uptime,
		}
		return render_template("qSpecific.html",**templateData)	
	else:	      
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'uptime':uptime,
		}
		return render_template('qSpecific.html', **templateData)	

@app.route('/query_between_DAYS',methods = ['POST', 'GET'])
def query_between_DAYS():
	if request.method == 'POST':
		result = request.form
		resp = getFreelSpecificDAYS(result['year'],result['month'],result['day1'],result['day2'])
		lhour = last_hour()
		lday = last_day()
		llog = last_log()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'resp':resp,
		  'result':result,
		  'uptime':uptime,
		}
		return render_template("qbetweenDAYS.html",**templateData)	
	else:	      
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'uptime':uptime,
		}
		return render_template('qbetweenDAYS.html', **templateData)		

@app.route('/device')
def device():
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'uptime':uptime,
		}
		return render_template('device.html', **templateData)

@app.route('/project')
def project():
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'uptime':uptime,
		}
		return render_template('project.html', **templateData)		

@app.route('/',methods = ['POST', 'GET'])
def index():
		lhour = last_hour()
		llog = last_log()
		lday = last_day()
		ltime = local_time()
		uptime = getUptime()
		obs = owm.weather_at_id(4945486)
		w = obs.get_weather()
		status = w.get_status()
		temp = w.get_temperature('fahrenheit')
		temp['temp'] = int(temp['temp'])
		templateData = {
		  'lhour'	: lhour,
		  'llog'	: llog,
		  'ltime'	: ltime,
		  'lday':lday,
		  'uptime':uptime,
		  'status': status,
		  'temp':temp,
		}
		return render_template('index.html', **templateData)



if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True,port=5000)
