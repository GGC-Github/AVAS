#!/usr/bin/python3
import os
import makescript
import printutil
import re

def codeParser(codeList):
	totalList = []
	for code in codeList:
		reg = re.findall(r'(\w+)-(\w+)', code)
		if len(reg) == 0 or (len(reg) == 1 and '~' in code):
			return None

		if len(reg) == 2:
			listTmp = ["{}-{:02}".format(reg[0][0], x) for x in range(int(reg[0][1]), int(reg[1][1]) + 1)]
			totalList.extend(listTmp)
		elif len(reg) == 1 and reg[0][1].lower() == 'all':
			totalList = ["{}-{:02}".format(reg[0][0], x) for x in range(1, 73 + 1)]
			break
		else:
			if isinstance(code, list):
				totalList.extend(code)
			else:
				totalList.append(code)
	totalList = list(set(totalList))
	totalList.sort()
	return totalList

def main():
	print('[Start Collect Module]')
	fileName = 'AVAS.yaml'
	getPwd = os.getcwd()
	fullPath = getPwd + '/' + fileName
	print('\nConfiguratin File Path : ' + fullPath)
	try:
		if os.path.isfile(fullPath):
			doc = printutil.readConfig(fullPath)
			if doc is not None:
				fullCode = codeParser(doc['assetCode'])
				if fullCode is not None:
					makescript.mergeScript(doc, fullCode, getPwd)
				else:
					printutil.printUsage('Error : Code Parser')
			else:
				printutil.printUsage('Error : Config Parser');
		else:
			printutil.printUsage('Error : Not Found AVAS.yaml File')
	except Exception as err:
		printutil.printUsage(err)

if __name__ == '__main__':
	main()
