#!/usr/bin/env python3
import codeanalysisLinuxFunc
import codeanalysisWindowsFunc


def assetDistribution(code, key, fileList, infoList, sysList, codeMap):
	if sysList['osType'].lower() == 'linux':
		return getattr(codeanalysisLinuxFunc, 'analysis' + code)(key, fileList, infoList, sysList, codeMap)
	elif sysList['osType'].lower() == 'windows':
		return getattr(codeanalysisWindowsFunc, 'analysis' + code)(key, fileList, infoList, sysList, codeMap)
