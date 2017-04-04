from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")


    # CREATE DATABASE can't run inside a transaction
try:
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()
#cur.execute("Select 1 from tcount") != ERROR:

	cur.execute("CREATE DATABASE tcount")
	cur.close()
	conn.close()
except:
	pass

#Connecting to tcount

conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

#Create a Table
#The first step is to create a cursor.

cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS tweetwordcount;''')
conn.commit()

#try:
cur = conn.cursor()
cur.execute('''CREATE TABLE tweetwordcount
	(word TEXT PRIMARY KEY     NOT NULL,
	count INT     NOT NULL);''')
conn.commit()
#except:
#	pass

cur = conn.cursor()

class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()


    def process(self, tup):
        word = tup.values[0]

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])
       	uCount = self.counts[word]
       	uWord = word


	if uCount != 1:

		cur.execute("UPDATE tweetwordcount SET count=%s WHERE word=%s", (uCount, uWord))
		conn.commit()
        else:
		cur.execute("INSERT INTO tweetwordcount (word,count) \
        	VALUES (%s, %s)", (uWord, uCount))
        	conn.commit()        

        # Log the count - just to see the topology running
#self.log('%s: %d' % (word, self.counts[word]))

#Select
cur.execute("SELECT word, count from tweetwordcount")
records = cur.fetchall()
for rec in records:
   print ("word = ", rec[0])
   print ("count = ", rec[1], "\n")
conn.commit()

#conn.close()


