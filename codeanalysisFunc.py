#!/usr/bin/env python3
import codeanalysisBase

class analysislinux001(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		fullString = [self.code, '양호', {}]
		self.stat = {}
		resultCnt = 0
		for name in ['ssh', 'telnet']:
			flagCnt = 0
			flagCnt += self.processCheck(name)
			if 'ssh' in name: 
				flagCnt += self.portCheck(':22', name)
				flagCnt += self.systemctlCheck(['ssh.service', 'sshd.service'], name)
			else:
				flagCnt += self.portCheck(':23', name)
				flagCnt += self.systemctlCheck(['telnet.service', 'telnetd.service'], name)
			if flagCnt > 0:
				if 'ssh' in name:
					if '/etc/ssh/sshd_config' in self.fileList.keys():
						sshFlag = self.fileDataCheck('/etc/ssh/sshd_config', 1, 'exist', '^[\t ]*PermitRootLogin\s\S+$', 'PermitRootLogin')
						if sshFlag == 0:
							resultCnt += self.dataStrGetValue('/etc/ssh/sshd_config', '^[\t ]*PermitRootLogin\s(\S+)', 'no', '!')
					else:
						self.stat.update( { '/etc/ssh/sshd_config' : 'Not Found Configuration File(!)' } )
				else:
					if '/etc/pam.d/remote' in self.fileList.keys():
						secuFlag = self.fileDataCheck('/etc/pam.d/remote', 1, 'exist', '^[\t ]*auth\s.*pam_securetty\.so', 'pam_securetty.so')
					elif '/etc/pam.d/login' in self.fileList.keys():
						secuFlag = self.fileDataCheck('/etc/pam.d/login', 1, 'exist', '^[\t ]*auth\s.*pam_securetty\.so', 'pam_securetty.so')
					else:
						self.stat.update( { '/etc/pam.d/remote' : 'Not Found Configuration File(!)' } )
						self.stat.update( { '/etc/pam.d/login' : 'Not Found Configuration File(!)' } )
						resultCnt += 1
					if secuFlag == 0:
						if '/etc/securetty' in self.fileList.keys():
							resultCnt += self.fileDataCheck('/etc/securetty', 0, '!exist', '^[\t ]*pts\s+', 'pts')
						else:
							self.stat.update( { '/etc/seuretty' : 'Not Found Configuration File(!)' } )
							resultCnt += 1

		if resultCnt > 0:
			fullString[1] = '취약'
		fullString[2] = self.stat
		return fullString
			
class analysislinux003(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		fullString = [self.code, '양호', {}]
		self.stat = {}
		resultCnt = 0
		notfoundCnt = 0
		denyFile = ['/etc/pam.d/system-auth',\
					'/etc/pam.d/password-auth',\
					'/etc/pam.d/common-auth',\
					'/etc/pam.d/common-account']

		for name in denyFile:
			if name in self.fileList.keys():
				tallyFlag = self.fileDataCheck(name, 1, 'exist', '^auth\s+(?:required|requisite)\s+\S*(?:pam_tally|pam_tally2|pam_faillock)\.so.*$', 'deny')
				if tallyFlag == 0:
					resultCnt += self.dataNumGetValue(name, 'deny=([0-9]+)', 5, '<')
				else:
					resultCnt += 1
			else:
				self.stat.update( { name : 'Not Found Configuration File(!)' } )
				notfoundCnt += 1

		if resultCnt > 0 or notfoundCnt == 4:
			fullString[1] = '취약'
		fullString[2] = self.stat
		return fullString

class analysislinux007(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		fullString = [self.code, '양호', {}]
		self.stat = {}
		bResult = True

		if '/etc/passwd' in self.fileList.keys():
			bResult = self.fileStatCheck('/etc/passwd', '644', 'root', '<=')
		else:
			self.stat.update( { '/etc/passwd' : 'Not Found /etc/passwd File' } )

		if not bResult:
			fullString[1] = '취약'

		fullString[2] = self.stat
		return fullString

class analysislinux008(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		fullString = [self.code, '양호', {}]
		self.stat = {}
		bResult = True

		if '/etc/shadow' in self.fileList.keys():
			bResult = self.fileStatCheck('/etc/shadow', '400', 'root', '<=')
		else:
			self.stat.update( { '/etc/shadow' : 'Not Found /etc/passwd File' } )

		if not bResult:
			fullString[1] = '취약'

		fullString[2] = self.stat
		return fullString

class analysislinux031(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		fullString = [self.code, '양호', {}]
		self.stat = {}
		resultCnt = 0

		fullString[2] = self.stat
		return fullString

class analysislinux032(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		fullString = [self.code, '양호', {}]
		self.stat = {}
		resultCnt = 0

		fullString[2] = self.stat
		return fullString

class analysislinux042(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		fullString = [self.code, '리뷰', {}]
		self.stat = {}
		keyList = ['OS_VERSION', 'OS_KERNEL_VERSION']

		for key in keyList:
			if key in self.infoList.keys():
				self.stat.update( { key : self.infoList[key] } )

		fullString[2] = self.stat
		return fullString

class analysislinux043(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		fullString = [self.code, '리뷰', {}]
		self.stat = {}
		resultCnt = 0

		fullString[2] = self.stat
		return fullString

