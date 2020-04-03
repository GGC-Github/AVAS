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
			fileList, infoList, sysList = utility.xmlResultFileParser(os.path.join(fullPath, resultFile))
			for key in sorted(infoList.keys()):
				codeMap = getattr(codemapping, sysList['osType'].lower() + key[0] + 'codeMap')
				code = codeMap[key][0]
				a = getattr(codeanalysisFunc, 'analysis' + code)(key, fileList, infoList[key], sysList)
				tmp = a.analysisFunc()
				if tmp is not None:
					print(tmp[0] + '\n' + tmp[1])
					if tmp[2] is not None:
						for key in tmp[2].keys():
							print(tmp[2][key])
				else:
					print(tmp)

	except Exception:
		print(traceback.format_exc())
