from plugins import Plugin


class windowsosw35(Plugin):
	def __init__(self):
		super().__init__()
		self.code = "W-35"
		self.codeScript = """
echo     ^<infoElement code="%CODE035%"^> >> %RESULT_COLLECT_FILE%

reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RemoteRegistry" /s /v Start > remote_reg_tmp.txt
if "%ERRORLEVEL%" == "0" (
    call :base64encode remote_reg_tmp.txt
    echo         ^<command name="REMOTE_REGISTRY_REG"^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
    for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
    echo         ^]^]^>^</command^> >> %RESULT_COLLECT_FILE%
)
if exist remote_reg_tmp.txt (
    del /q remote_reg_tmp.txt
)

echo     ^</infoElement^> >> %RESULT_COLLECT_FILE%

echo %CODE035% Collect		
		"""
		self.codeExcute = "set CODE035=W-35"
		self.description = {
			'Category': '로그 관리',
			'Name': '원격으로 엑세스 할 수 있는 레지스트리 경로',
			'Important': '상',
			'ImportantScore': '3',
			'Criterion': '양호 : Remote Registry Service가 중지되어 있는 경우\n'
			             '취약 : Remote Registry Service가 사용 중인 경우',
			'ActionPlan': '불필요 시 서비스 중지 및 사용 안함으로 설정'
		}
		self.fullString = [self.code, '양호', self.stat, self.description]

	def analysisFunc(self, sysInfo, infoDict, fileDict):
		vulCnt = 0
		chkNum = 0
		desStr = """
[참고]
서비스 시작유형(재부팅시 서비스 구동여부)
자동(재부팅시 시작됨)    - 2
수동(재부팅시 수동)      -  3
사용안함(재부팅시 중지됨) -  4
		        """
		chkNum += self.serviceCheck(sysInfo, ['Remote Registry'], 'Remote Registry')
		if chkNum > 0:
			serviceStr = self.stat['Remote Registry_SYS'].replace('\n', '')
			self.stat.update({'Remote Registry_SYS': f'{serviceStr} Service Running(!)\n'})
			vulCnt += 1

		if infoDict:
			if 'REMOTE_REGISTRY_REG' in infoDict[0]:
				vulCnt += self.cmdStrGetValue('CMD:Remote Registry 서비스 시작 유형', infoDict[0], 'REMOTE_REGISTRY_REG',
				                              '^[ \t]*Start.*0x(.)$', '2', '==')
				valueStr = self.stat['CMD:Remote Registry 서비스 시작 유형']
				self.stat.update({'CMD:Remote Registry 서비스 시작 유형': f'{valueStr} {desStr}\n'})
		else:
			self.stat.update({'CMD:Remote Registry 서비스 시작 유형': '- Not Found Remote Registry Start Result\n'})

		if vulCnt > 0:
			self.fullString[1] = '취약'

		return self.fullString
