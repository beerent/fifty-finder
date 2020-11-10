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

# takes a string as input
# removes non ascii characters, needless spaces and undesired tokens
def rowToCleanArray(row):
	row = row.strip()
	row = ''.join([j if ord(j) < 128 else '' for j in row])
	splitString = row.split(" ")
	splitString = [x for x in splitString if x != "" and x != "Edited"]

	return splitString

# returns true if timestamp character is in string
# w = week, d = day, h = hour, etc.
def getTimestampCharacter(s):
	if "w" in s:
		return "w"
	if "d" in s:
		return "d"
	if "h" in s:
		return "h"
	if "m" in s:
		return "m"
	if "s" in s:
		return "s"

	return None

# accepts a row split into a list from the file
# returns true if the row represents a row that is followed by a user's name
# 
# we look for a comment with a time associated, for example " Reply 1d"
# this function looks to see if the final token is a time stamp (in this example, 1d)
def isRowBeforeUsersName(searchList):
	if len(searchList) == 0:
		return False

	lastElement = searchList[-1]

	timestampChar = getTimestampCharacter(lastElement)
	if (timestampChar == None):
		return False

	potentialNumber = lastElement.split(timestampChar)
	if len(potentialNumber) == 0:
		return False

	potentialNumber = potentialNumber[0]

	if not isNumber(potentialNumber):
		return False

	return True

def getUsersFromFile(filePath):
	users = set()

	with open(filePath) as f:
		rows = f.readlines()

	i = 0
	while i+1 < len(rows):
		usersName = rows[i].strip()
		i+=1

		if usersName == "" or usersName == "\n":
			continue

		searchingForNextUser = True
		while searchingForNextUser:
			currentRow = rows[i]
			searchList = rowToCleanArray(currentRow)
			i+=1

			if isRowBeforeUsersName(searchList):
				users.add(usersName)
				searchingForNextUser = False

	return users

def writeUsersToFile(users, filePath):
	with open(filePath, 'wb') as outfile:
		wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
		for user in users:
			wr.writerow([user])

def logResults(users, outputFile, runtime):
	print ""
	print ""
	print "fifty finder winner finder results:"
	print "total users:\t" + str(len(users))
	print "bakers guess:\t" + random.choice(tuple(users))
	print "execution time:\t" + str(runtime)[0:8]
	print "file saved:\t" + outputFile
	print ""
	print ""
	print "           _   _            _           _             "
	print "          | | | |          | |         | |            "
	print "  ______  | |_| |__   ___  | |__   __ _| | _____ _ __ "
	print " |______| | __| '_ \\ / _ \\ | '_ \\ / _` | |/ / _ \\ '__|"
	print "          | |_| | | |  __/ | |_) | (_| |   <  __/ |   "
	print "           \\__|_| |_|\\___| |_.__/ \\__,_|_|\\_\\___|_|"

def main():
	if len(sys.argv) != 2:
		print "missing filename!"
		print "example: 'python fiftyfinder.py bait23.txt'"
		exit(1)

	inputFile = sys.argv[1]
	outputFile = inputFile.split(".")[0] + '.csv'

	start = time.time()
	users = getUsersFromFile(inputFile)
	writeUsersToFile(users, outputFile)
	end = time.time()

	logResults(users, outputFile, end - start)

if __name__ == "__main__":
    main()
