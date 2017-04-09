import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")


conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

cur = conn.cursor()

userInMin = raw_input("Minimum Count: ")
userInMax = raw_input("Maximum Count: ")

cur.execute("SELECT word, count from tweetwordcount  where count >= %s AND count <= %s order by count desc" % (userInMin,userInMax))
records = cur.fetchall()
for rec in records:
 print "word = ", rec[0]
 print "count = ", rec[1], "\n"
 conn.commit()
