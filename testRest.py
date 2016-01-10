# Automated Testing procedures for the MIS interface and backend.
# Created by Brett Davidoff
# January 2016
# For more information, email @ BDavidoff3@gmail.com


import urllib, urllib2
import datetime
from random import randrange
from time import sleep

ORDERNUMBER        = raw_input("enter a vaild order number: ")				#open up source for page and search for 'data-og-order'
SUBSCRIPTIONNUMBER = raw_input("enter a valid subscription number: ")		#open up source for page and search for 'data-og-subscription'


def callStaging(cmd, type, extra=""):
	url = "https://staging.v2.ordergroove.com/" + type + cmd + "?merchant_id=d0fe14a4e081a81fa5d8ea72df110f34&merchant_user_id=TestCust&merchant_user_hash=h3who0E16IY%3D&cb=1309445&request_type=jsonp" + extra
	# print url
	try:
		return urllib2.urlopen(url).read()
	except urllib2.HTTPError:
		return "ERROR: Failed to connect to server"

def callChangeDate(dateString):
	return callStaging('change_date%s' % dateString, 'order/%s/' % ORDERNUMBER)

def callSendNow(orderNum):
	return callStaging('/send_now', 'order/%s' % orderNum)

def callReactivate(startDate, frequency, every, everyPeriod):
	timeString = "&start_date=%s&frequency_days=%s&every=%s&every_period=%s" % (startDate, frequency, every, everyPeriod)
	return callStaging("reactivate/", "subscription/%s/" % SUBSCRIPTIONNUMBER, timeString)

def callDeactivate(reason):
	return callStaging("cancel/", "subscription/%s/" % SUBSCRIPTIONNUMBER, "&reason=" + reason)
	
def testDates():
	file = open("testDates.txt", "w")
	badDates = ["/%s/%s/%s" % (randrange(0,100), randrange(0,100), randrange(0,10000)) for x in range(0, 100)]
	
	
	#get all dates in the year including today
	date_list = [(datetime.datetime.today() + datetime.timedelta(days=x)).strftime('/%m/%d/%Y') for x in range(0, 365)]
	print "testing REAL dates"
	for x in date_list:

		result = callChangeDate(x)
		
		file.write("Date: " + x + "\t" + result + "\n")
		print "Date: " + x + "\t" + result + "\n"
	print "testing FAKE dates"
	file.write("\n\n\nBAD DATES\n\n\n")
	for x in badDates:
		result = callChangeDate(x)
		
		file.write("Date: " + x + "\t" + result + "\n")
		print "Date: " + x + "\t" + result + "\n"
	file.close()
	
def testSubmits():
	file = open("testSubmits.txt", "w")
	randomIds = [str(randrange(100000, 1000000)) for x in range(0, 100)]
	
	#add a single known working ID
	randomIds.append(ORDERNUMBER)
	
	for x in randomIds:
		result = callSendNow(x)
		file.write("ID: " + x + "\t" + result + "\n")
		print "ID: " + x + "\t" + result + "\n"
	file.close()
	
def testReactivates():
	file = open("testReactivates.txt", "w")
	cancelReasons = ['account_trouble%7C', 'reorganizing%7C', 'expensive%7C', 'account_trouble%7C', 'overstocked%7C', 'shipping_fees%7C']
	for x in cancelReasons:
		print "testing: %s" % x
		startDate   = "%s-%s-%s" % (randrange(2016, 4001), randrange(1,13), randrange(1,28))
		frequency   = randrange(1, 100)
		every       = randrange(1,15)
		everyPeriod = randrange(1,15)
		
		reactiveResult = callReactivate(startDate, frequency, every, everyPeriod)
		deactiveResult = callDeactivate(x)
		
		file.write("%s\t%s %s %s \t %s\n" % (startDate, frequency, every, everyPeriod, reactiveResult))
		print "%s\t%s %s %s \t %s\n" % (startDate, frequency, every, everyPeriod, reactiveResult)
		
		file.write('%s\t%s\n' % (x, deactiveResult))
		print '%s\t%s\n' % (x, deactiveResult)
	file.close()
	
print "start"
testDates()
testSubmits()
testReactivates()
print "complete"