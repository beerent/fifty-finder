import sys
import csv
import time
import random

def isNumber(input):
	try:
		val = int(input)
		return True
	except ValueError:
		return False

def cleanAndSplitEndSearchString(s):
	s = s.strip()
	s = ''.join([j if ord(j) < 128 else '' for j in s])
	splitString = s.split(" ")
	splitString = [x for x in splitString if x != "" and x != "Edited"]

	return splitString

def getSplitChar(lastElement):
	splitChar = None

	if ("w" in lastElement):
		splitChar = "w"
	elif ("d" in lastElement):
		splitChar = "d"
	elif ("h" in lastElement):
		splitChar = "h"
	elif ("m" in lastElement):
		splitChar = "m"
	elif ("s" in lastElement):
		splitChar = "s"

	return splitChar

if len(sys.argv) != 2:
	print "missing filename!"
	print "example: 'python fiftyfinder.py bait23.txt'"
	exit(1)

start = time.time()
filename = sys.argv[1]

with open(filename) as f:
	content = f.readlines()

users = []

i = 0
while i+1 < len(content):
	firstEntry = content[i].strip()
	i+=1

	if firstEntry == "" or firstEntry == "\n":
		continue

	while True:
		searchList = cleanAndSplitEndSearchString(content[i])
		i+=1

		if len(searchList) == 0:
			continue

		lastElement = searchList[-1]
		splitChar = getSplitChar(lastElement)
		if (splitChar == None):
			continue

		potentialNumber = lastElement.split(splitChar)
		if len(potentialNumber) == 0:
			continue

		potentialNumber = potentialNumber[0]

		if (isNumber(potentialNumber)):
			if (firstEntry not in users):
				users.append(firstEntry)
			break

with open(filename.split(".")[0] + '.csv', 'wb') as outfile:
	wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
	for user in users:
		wr.writerow([user])

end = time.time()

print ""
print ""
print "fifty finder winner finder results:"
print "total users:\t" + str(len(users))
print "bakers guess:\t" + users[random.randint(0,len(users)-1)]
print "execution time:\t" + str(end - start)[0:8]
print "file saved:\t" + str(filename.split(".")[0] + '.csv')
print ""
print ""
print "           _   _            _           _             "
print "          | | | |          | |         | |            "
print "  ______  | |_| |__   ___  | |__   __ _| | _____ _ __ "
print " |______| | __| '_ \\ / _ \\ | '_ \\ / _` | |/ / _ \\ '__|"
print "          | |_| | | |  __/ | |_) | (_| |   <  __/ |   "
print "           \\__|_| |_|\\___| |_.__/ \\__,_|_|\\_\\___|_|"