__author__ = "Vaibhaw Raj"

import sys
from Stemmer import printSummary
from Stemmer import generateGrammer
from Parser import earleyParser

def readStdin():
	inputLines = []
	lineNo = 0
	for x in sys.stdin:
		lineNo += 1
		inputLines.append((lineNo,x))
	return inputLines

def normalizeInput(inputLines):
	outInputLines = []
	for line in inputLines:
		lineInput = line[1]
		lineInputLen = len(lineInput)

		#Remove Line Feed
		if lineInput[lineInputLen - 1] == '\n':
			lineInput = lineInput[:lineInputLen-1]

		#Handle comments
		if '#' in lineInput:
			# Strip anything comming after #
			lineInput = lineInput.split('#')[0]

		#Strip White space
		lineInput = lineInput.strip()

		#Handle Empty Lines
		if(len(lineInput)==0):
			continue

		outInputLines.append((line[0],lineInput))
	return outInputLines

inputLines = normalizeInput(readStdin())

print("Stemmer:")
for line in inputLines:
	printSummary(line[0],line[1])
print("ENDFILE")

# Parsing Grammer Rule
inputString = " ".join([ x[1] for x in inputLines])

print("")

grammer_g = generateGrammer(inputString)
sentence = grammer_g[0]
grammer = grammer_g[1]

print("Parsed Chart:")
earleyParser(sentence, grammer)

