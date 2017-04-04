import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")


conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

cur = conn.cursor()

userIn = raw_input("Search word: ")
#print(userIn)

if userIn == '':
  cur.execute("SELECT word, count from tweetwordcount order by word asc")
  records = cur.fetchall()
  for rec in records:
   print "word = ", rec[0]
   print "count = ", rec[1], "\n"
   conn.commit()
else:
  cur.execute("SELECT word, count from tweetwordcount  where word = %s",(userIn))
  records = cur.fetchall()
  for rec in records:
   print "word = ", rec[0]
   print "count = ", rec[1], "\n"
   conn.commit()

