from plugins import Plugin


class linuxosu32(Plugin):
	def __init__(self):
		super().__init__()
		self.code = "U-32"
		self.codeScript = """
linux032() {
	code=$1
	xml_infoElement_tag_start "$code"

	xml_fileInfo_write "/etc/sendmail.cf"
	xml_fileInfo_write "/etc/mail/sendmail.cf"

	xml_infoElement_tag_end "$code"
}
		"""
		self.codeExcute = "linux032 U-32"
		self.description = {
			'Category': '서비스 관리',
			'Name': '일반사용자의 Sendmail 실행 방지',
			'Important': '상',
			'ImportantScore': '3',
			'Criterion': '양호 : SMTP 서비스 미사용 또는, 일반 사용자의 Sendmail 실행 방지가 설정된 경우\n'
			'취약 : SMTP 서비스 사용 및 일반 사용자의 Sendmail 실행 방지가 설정되어 있지 않은 경우',
			'ActionPlan': 'Sendmail 서비스를 사용하지 않을 경우 서비스 중지\n'
			              'Sendmail 서비스를 사용 시 sendmail.cf 설정파일에 restrictqrun 옵션 추가 설정'
		}
		self.fullString = [self.code, '양호', self.stat, self.description]

	def analysisFunc(self, sysInfo, infoDict, fileDict):
		vulCnt = 0
		chkNum = 0
		chkNum += self.processCheck(sysInfo, 'sendmail')
		chkNum += self.serviceCheck(sysInfo, ['sendmail.service'], 'sendmail', 'loaded active')

		if chkNum > 0:
			chkFlag, dictKey = self.getFileName(infoDict, fileDict, 'sendmail.cf')
			if chkFlag:
				if self.getConfig(dictKey, '^[\t ]*O\\s+PrivacyOptions\\s*=\\s*.+$', 'PrivacyOptions', 'exist'):
					vulCnt += self.compStrValue(dictKey, '^[\t ]*O\\s+PrivacyOptions\\s*=\\s*(.+$)', 'restrictqrun', 'in')
		else:
			vulCnt += 1

		if vulCnt == 0:
			self.fullString[1] = '취약'

		return self.fullString
