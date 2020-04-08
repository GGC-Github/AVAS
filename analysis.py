#!/usr/bin/env python3
import os
import traceback
import codemapping
import codeanalysisFunc
import utility
import excelutility

if __name__ == '__main__':
	try:
		print('[ Start Analysis Module ]\n')
		fullPath = os.path.join(os.getcwd(), 'inputResult')
		print('Input Result Collection XML File Directory : ' + fullPath + '\n')
		fullFileList = os.listdir(fullPath)
		print('[ Result File List ]\n')
		resultNum = 1
		for resultFile in fullFileList:
			if 'README.md' == resultFile:
				continue
			fileList, infoList, sysList = utility.xmlResultFileParser(
											os.path.join(fullPath, resultFile))
			print('##### Result xml File Parsing Success!')
			analysisRes = []
			for key in sorted(infoList.keys()):
				codeMap = getattr(codemapping, sysList['osType'].lower() + key[0]\
								+ 'codeMap')
				code = codeMap[key][0]
				a = getattr(codeanalysisFunc, 'analysis' + code)(key, fileList,
							infoList[key], sysList)
				analysisRes.append(a.analysisFunc())

			print('##### Total Item Analysis Success!')
			excelutility.makeExcelReport(analysisRes, sysList, resultNum)

			print('##### Final Result Report Successfully Created!\n')
			resultNum += 1

		print('[ End Analysis Module ]')

	except Exception:
		print(traceback.format_exc())
