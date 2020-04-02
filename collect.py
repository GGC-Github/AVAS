#!/usr/bin/env python3

import os
import re
import traceback
import utility

def main():
	print('[Start Collect Module]')
	fileName = 'AVAS.yaml'
	getPwd = os.getcwd()
	fullPath = os.path.join(getPwd, fileName)
	try:
		print('\nConfiguratin File Path : ' + fullPath)
		doc = utility.readConfig(fullPath)
		fullCode = utility.codeParser(doc['assetCode'])
		utility.mergeScript(doc, fullCode, getPwd)
	except Exception:
		utility.printUsage(traceback.format_exc())

if __name__ == '__main__':
	main()
