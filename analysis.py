#!/usr/bin/env python3
import os
import traceback
import codemapping
import utility

class InfoAnalysis:
	fileCollectList = {}
	infoCollectList = {}
	sysInfo = {}

def main():
	try:
		print('[ Start Analysis Module ]\n')
		fullPath = os.path.join(os.getcwd(), 'inputResult')
		print('Input Result Collection XML File Directory : ' + fullPath + '\n')
		fullFileList = os.listdir(fullPath)
		print('[ Result File List ]\n')
		for resultFile in fullFileList:
			a = InfoAnalysis()
			utility.xmlResultFileParser(os.path.join(fullPath, resultFile), a)
			for code in a.infoCollectList.keys():
				a.infoCollectList[code]['analyFunc']()
			a.fileCollectList.clear()
			a.infoCollectList.clear()
			a.sysInfo.clear()
			
	except Exception:
		print(traceback.format_exc())

if __name__ == '__main__':
	main()
