#!/usr/bin/env python3
import os
import traceback
import codemapping
import codeanalysisFunc
import utility

if __name__ == '__main__':
	try:
		print('[ Start Analysis Module ]\n')
		fullPath = os.path.join(os.getcwd(), 'inputResult')
		print('Input Result Collection XML File Directory : ' + fullPath + '\n')
		fullFileList = os.listdir(fullPath)
		print('[ Result File List ]\n')
		for resultFile in fullFileList:
			fileList, infoList, sysList = utility.xmlResultFileParser(\
											os.path.join(fullPath, resultFile)\
										  )
			analysisRes = []
			for key in sorted(infoList.keys()):
				codeMap = getattr(codemapping, sysList['osType'].lower() + key[0]\
								+ 'codeMap')
				code = codeMap[key][0]
				a = getattr(codeanalysisFunc, 'analysis' + code)(key, fileList,\
							infoList[key], sysList)
				analysisRes.append(a.analysisFunc())
			for b in analysisRes:
				print('\n')
				print(b)

	except Exception:
		print(traceback.format_exc())
