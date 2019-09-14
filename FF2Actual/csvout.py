import csv
import sqlite3

conn=sqlite3.connect("FFpir.db")
c=conn.cursor()

data = c.execute("select strftime('%m',timestamp) as Month,strftime('%d',timestamp) as Day,strftime('%H',timestamp) as Hour,count(*) as Count from pir group by strftime('%d %H',timestamp) order by strftime('%m %d %H',timestamp) desc;")
with open('data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Month','Day','Hour','Count'])
    writer.writerows(data)