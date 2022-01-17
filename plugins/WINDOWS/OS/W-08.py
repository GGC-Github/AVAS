from plugins import Plugin


class windowsosw08(Plugin):
	def __init__(self):
		super().__init__()
		self.code = "W-08"
		self.codeScript = """
call :xml_infoElement_tag_start %CODE008%

net share | more > default_share_tmp.txt
if "%ERRORLEVEL%" == "0" call :xml_command_write default_share_tmp.txt, DEFAULT_SHARE
if exist default_share_tmp.txt del /q default_share_tmp.txt

reg query "HKLM\SYSTEM\CurrentControlSet\Services\lanmanserver\parameters" /s /v AutoShareServer > autoshare_server_reg_tmp.txt
if "%ERRORLEVEL%" == "0" call :xml_command_write autoshare_server_reg_tmp.txt, AUTOSHARE_SERVER_REG
if exist autoshare_server_reg_tmp.txt del /q autoshare_server_reg_tmp.txt

reg query "HKLM\SYSTEM\CurrentControlSet\Services\lanmanserver\parameters" /s /v AutoShareWks > autoshare_wks_reg_tmp.txt
if "%ERRORLEVEL%" == "0" call :xml_command_write autoshare_wks_reg_tmp.txt, AUTOSHARE_WKS_REG
if exist autoshare_wks_reg_tmp.txt del /q autoshare_wks_reg_tmp.txt

call :xml_infoElement_tag_end %CODE008%
"""
		self.codeExecute = "set CODE008=W-08"
		self.description = {
			'Category': '서비스 관리',
			'Name': '하드디스크 기본 공유 제거',
			'Important': '상',
			'ImportantScore': '3',
			'Criterion': '양호 : 레지스트리의 AutoShareServer(WinNT : AutoShareWks)가 0이며 기본 공유가 존재하지 않는 경우\n'
			'취약 : 레지스트리의 AutoShareServer(WinNT : AutoShareWks)가 1이거나 기본 공유가 존재하는 경우',
			'ActionPlan': '기본 공유 중지 후 레지스트리 값 설정(IPC$, 일반 공유 제외)'
		}
		self.fullString = [self.code, '양호', self.stat, self.description]

	def analysisFunc(self, sysInfo, infoDict, fileDict):
		resultCnt = 0
		keyList = {
			'CMD:기본 공유 설정 여부(net share)':
				['DEFAULT_SHARE', '^[\\S]+[ \t]+[\\S]+[ \t]+(.*)', '기본 공유|Default share', '|', 'net share'],
			'CMD:AutoShareServer 레지스트리 설정':
				['AUTOSHARE_SERVER_REG', '^[ \t]*AutoShareServer.*0x(.)$', '1', '!=', 'reg query AutoShareServer'],
			'CMD:AutoShareWks 레지스트리 설정':
				['AUTOSHARE_WKS_REG', '^[ \t]*AutoShareWks.*0x(.)$', '1', '!=', 'reg query AutoShareWks']
		}
		for key in keyList.keys():
			existFlag = False
			if infoDict:
				for info in infoDict:
					if keyList[key][0] in info:
						resultCnt += self.cmdStrGetValue(key, info, keyList[key][0], keyList[key][1],
						                                 keyList[key][2], keyList[key][3])
						existFlag = True
			if not existFlag:
				resultCnt += 1
				self.stat.update({key: f'- Not Found "{keyList[key][4]}" Result\n'})

		if resultCnt < 3:
			self.fullString[1] = '취약'

		return self.fullString
