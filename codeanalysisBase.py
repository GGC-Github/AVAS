from abc import *
import re
import utility

class analysisBase(metaclass=ABCMeta):
	def __init__(self, code, fileList, infoList, sysList):
		self.code = code
		self.fileList = fileList
		self.infoList = infoList
		self.sysList = sysList
		self.stat = {}

	@abstractmethod
	def analysisFunc(self):
		pass

	def processCheck(self, getValue):
		keyValue = "{}{}".format(getValue, 'PS')
		self.stat.update( { keyValue : ''.join("{} Not found Process\n".format(getValue)) })
		flag = 0
		if self.sysList['processInfo'] is not None:
			valueStr = ''.join("{}\n".format(line) \
						for line in self.sysList['processInfo'].split('\n') \
						if getValue in line)
			if valueStr != '':
				self.stat.update( { keyValue : valueStr } )
				flag = 1

		return flag

	def portCheck(self, getValue, srvName):
		keyValue = "{}{}".format(srvName, 'PORT')
		self.stat.update( { keyValue : ''.join("{} Not found Port\n".format(srvName)) })
		flag = 0
		if self.sysList['portInfo'] is not None:
			valueStr = ''.join("{}\n".format(line) \
						for line in self.sysList['portInfo'].split('\n') \
						if getValue in line)
			if valueStr != '':
				self.stat.update( { keyValue : valueStr } )
				flag = 1

		return flag

	def systemctlCheck(self, getValue, srvName):
		keyValue = "{}{}".format(srvName, 'SYS')
		self.stat.update( { keyValue : ''.join("{} Not found Service\n".format(srvName)) })
		flag = 0
		if self.sysList['systemctlInfo'] is not None:
			valueStr = ''.join("{}\n".format(line) \
						for line in self.sysList['systemctlInfo'].split('\n') \
						for value in getValue
						if value in line)
			if valueStr != '':
				self.stat.update( { keyValue : valueStr } )
				if 'loaded active' in self.stat[keyValue]:
					flag = 1
		return flag
	
	def fileDataCheck(self, fileName, defaultCnt, parseKey, pattern, confAttr):
		result = defaultCnt
		fileContent = self.fileList[fileName]
		self.stat.update( { fileName : ''.join("{} Not Found Configuration(!)".format(confAttr))} )
		if fileContent is not None:
			com = re.compile(pattern, re.MULTILINE)
			reg = re.findall(com, fileContent['fileData'])
			if reg:
				self.stat.update( { fileName : ''.join("{}\n".format(line) for line in reg) } )
				if parseKey == 'exist':
					result = 0
				elif parseKey == '!exist':
					self.stat.update( { fileName : ''.join("{}(!)\n".format(line) for line in reg) } )
					result = 1

		return result	

	def dataNumGetValue(self, name, pattern, compValue, compType):
		result = 0
		com = re.compile(pattern, re.MULTILINE)
		reg = re.findall(com, self.stat[name])
		if compType == '<':
			if reg and int(reg[0]) < compValue:
				self.stat.update( { name : ''.join("{}(!)\n".format(line) for line in self.stat[name]) } )
				result = 1
		elif compType == '>':
			if reg and int(reg[0]) > comValue:
				self.stat.update( { name : ''.join("{}(!)\n".format(line) for line in self.stat[name]) } )
				result = 1
		elif comType == '=':
			if reg and int(reg[0]) == comValue:
				self.stat.update( { name : ''.join("{}(!)\n".format(line) for line in self.stat[name]) } )
				result = 1

		return result

	def dataStrGetValue(self, name, pattern, compValue, compType):
		result = 0
		com = re.compile(pattern, re.MULTILINE)
		reg = re.findall(com, self.stat[name])
		if compType == '!':
			if reg and reg[0] != compValue:
				self.stat.update( { name : ''.join("{}(!)\n".format(line) for line in self.stat[name]) } )
				result = 1
		elif compType == '=':
			if reg and reg[0] == compValue:
				self.stat.update( { name : ''.join("{}(!)\n".format(line) for line in self.stat[name]) } )
				result = 1

		return result

	def fileStatCheck(self, fileName, compPerm, compOwner, compType):
		cmpOper = utility.OPS[compType]
		if 'fileRealStat' in self.fileList[fileName].keys():
			fileStat = self.fileList[fileName]['fileRealStat'].split('|')
#			self.stat.update( { fileName : "[ 권한 = {}({}), 소유자 = {}({}), 소유그룹 = {}({}) ]".format(fileStat[1], fileStat[0], fileStat[]) } )
			self.stat.update( { fileName : self.fileList[fileName]['fileRealStat']} )
			self.stat.update( { fileName : self.fileList[fileName]['fileStat']} )
		else:
			fileStat = self.fileList[fileName]['fileStat'].split('|')
			self.stat.update( { fileName : self.fileList[fileName]['fileStat']} )

		filePerm = fileStat[1]
		fileOwner = fileStat[5]
		permBool = True
		ownerBool = True
		resultBool = False

		if compPerm is not None:
			for i in range(0, len(filePerm)):
				if not cmpOper(filePerm[i], compPerm[i]):
					print(filePerm[i], compPerm[i])
					permBool = False
					break

		if compOwner is not None:
			if fileOwner != compOwner:
				ownerBool = False

		if permBool and ownerBool:
			resultBool = True

		return resultBool
