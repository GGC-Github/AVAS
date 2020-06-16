#!/usr/bin/env python3
import codeanalysisBase


class analysislinux001(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		resultCnt = 0
		for name in ['ssh', 'telnet']:
			flagCnt = 0
			flagCnt += self.processCheck(name)
			if 'ssh' in name: 
				flagCnt += self.portCheck(':22', name)
				flagCnt += self.serviceCheck(['ssh.service', 'sshd.service'], name, 'loaded active')
			else:
				flagCnt += self.portCheck(':23', name)
				flagCnt += self.serviceCheck(['telnet.service', 'telnetd.service'], name, 'loaded active')
			if flagCnt > 0:
				if 'ssh' in name:
					if '/etc/ssh/sshd_config' in self.fileList.keys():
						sshFlag = self.fileDataCheck(
							'/etc/ssh/sshd_config', 1, 'exist', '^[\t ]*PermitRootLogin\s\S+$', 'PermitRootLogin')
						if sshFlag == 0:
							resultCnt += self.dataStrGetValue(
								'/etc/ssh/sshd_config', '^[\t ]*PermitRootLogin\s(\S+)', 'no', '!=')
						else:
							self.stat.update(
								{'FILEDATA:/etc/ssh/sshd_config': '- PermitRootLogin Not Found Configuration\n'})
					else:
						self.stat.update({'FILEDATA:/etc/ssh/sshd_config': '- Not Found Configuration File(!)\n'})
				else:
					if '/etc/pam.d/remote' in self.fileList.keys():
						secuFlag = self.fileDataCheck(
							'/etc/pam.d/remote', 1, 'exist', '^[\t ]*auth\s.*pam_securetty\.so', 'pam_securetty.so')
					elif '/etc/pam.d/login' in self.fileList.keys():
						secuFlag = self.fileDataCheck(
							'/etc/pam.d/login', 1, 'exist', '^[\t ]*auth\s.*pam_securetty\.so', 'pam_securetty.so')
					else:
						self.stat.update(
							{'FILEDATA:/etc/pam.d/remote': '- Not Found Configuration File(!)\n'})
						self.stat.update(
							{'FILEDATA:/etc/pam.d/login': '- Not Found Configuration File(!)\n'})
						resultCnt += 1
					if secuFlag == 0:
						if '/etc/securetty' in self.fileList.keys():
							resultCnt += self.fileDataCheck('/etc/securetty', 0, '!exist', '^[\t ]*pts\s+', 'pts')
						else:
							self.stat.update({'FILEDATA:/etc/securetty': '- Not Found Configuration File(!)\n'})
							resultCnt += 1

		if resultCnt > 0:
			self.fullString[1] = '취약'
		self.fullString[2] = self.stat
		return self.fullString


class analysislinux003(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		resultCnt = 0
		notfoundCnt = 0
		denyFile = [
			'/etc/pam.d/system-auth',
			'/etc/pam.d/password-auth',
			'/etc/pam.d/common-auth',
			'/etc/pam.d/common-account']

		for name in denyFile:
			if name in self.fileList.keys():
				tallyFlag = self.fileDataCheck(
					name, 1, 'exist',
					'^auth\s+(?:required|requisite)\s+\S*(?:pam_tally|pam_tally2|pam_faillock)\.so.*$', 'deny'
				)
				if tallyFlag == 0:
					resultCnt += self.dataNumGetValue(name, 'deny=([0-9]+)', 5, '<')
				else:
					resultCnt += 1
			else:
				self.stat.update({f'FILEDATA:{name}': '- Not Found Configuration File\n'})
				notfoundCnt += 1

		if resultCnt > 0 or notfoundCnt == 4:
			self.fullString[1] = '취약'
		self.fullString[2] = self.stat
		return self.fullString


class analysislinux007(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		bResult = True

		if '/etc/passwd' in self.fileList.keys():
			bResult = self.fileStatCheck('/etc/passwd', '644', 'root', '<=')
		else:
			self.stat.update({'FILEPERM:/etc/passwd': '- Not Found /etc/passwd File\n'})

		if not bResult:
			self.fullString[1] = '취약'

		self.fullString[2] = self.stat
		return self.fullString


class analysislinux008(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		bResult = True

		if '/etc/shadow' in self.fileList.keys():
			bResult = self.fileStatCheck('/etc/shadow', '400', 'root', '<=')
		else:
			self.stat.update({'FILEPERM:/etc/shadow': '- Not Found /etc/shadow File\n'})

		if not bResult:
			self.fullString[1] = '취약'

		self.fullString[2] = self.stat
		return self.fullString


class analysislinux031(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		dataFile = None
		resultCnt = 1
		flagCnt = 0

		flagCnt += self.processCheck('sendmail')
		flagCnt += self.serviceCheck(['sendmail.service'], 'sendmail', 'loaded active')

		if flagCnt > 0:
			if '/etc/mail/sendmail.cf' in self.fileList.keys():
				dataFile = '/etc/mail/sendmail.cf'
			elif '/etc/sendmail.cf' in self.fileList.keys():
				dataFile = '/etc/sendmail.cf'
			else:
				self.stat.update({'FILEDATA:/etc/mail/sendmail.cf': '- Not Found Configuration File(!)\n'})
				self.stat.update({'FILEDATA:/etc/sendmail.cf': f'- Not Found Configuration File(!)\n'})

			if dataFile is not None:
				resultCnt = self.fileDataCheck(dataFile, 1, 'exist', '^R.*550 Relaying denied.*$', 'Relaying denied')

			if resultCnt > 0:
				self.fullString[1] = '취약'

		self.fullString[2] = self.stat
		return self.fullString


class analysislinux032(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		dataFile = None
		resultCnt = 0
		flagCnt = 0

		flagCnt += self.processCheck('sendmail')
		flagCnt += self.serviceCheck(['sendmail.service'], 'sendmail', 'loaded active')

		if flagCnt > 0:
			if '/etc/mail/sendmail.cf' in self.fileList.keys():
				dataFile = '/etc/mail/sendmail.cf'
			elif '/etc/sendmail.cf' in self.fileList.keys():
				dataFile = '/etc/sendmail.cf'
			else:
				self.stat.update({'FILEDATA:/etc/mail/sendmail.cf': '- Not Found Configuration File(!)\n'})
				self.stat.update({'FILEDATA:/etc/sendmail.cf': '- Not Found Configuration File(!)\n'})

			if dataFile is not None:
				privCnt = self.fileDataCheck(
					dataFile, 1, 'exist', '^[\t ]*O\s+PrivacyOptions\s*=\s*.+$', 'PrivacyOptions')
				if privCnt == 0:
					resultCnt += self.dataStrGetValue(dataFile, '^[\t ]*O\s+PrivacyOptions\s*=\s*(.+$)', 'restrictqrun', 'not in')
			if resultCnt > 0:
				self.fullString[1] = '취약'

		self.fullString[2] = self.stat
		return self.fullString


class analysislinux042(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		self.fullString[1] = '리뷰'
		keyList = {
			'OS_VERSION': 'OS 버전',
			'OS_KERNEL_VERSION': 'OS 커널 버전'
		}

		for key in keyList.keys():
			if key in self.infoList.keys():
				self.stat.update({f'CMD:{keyList[key]}': self.infoList[key]})

		self.fullString[2] = self.stat
		return self.fullString


class analysislinux043(codeanalysisBase.analysisBase):
	def analysisFunc(self):
		self.fullString[1] = '리뷰'
		self.stat.update({'NULLKEY': ''})
		self.fullString[2] = self.stat
		return self.fullString
