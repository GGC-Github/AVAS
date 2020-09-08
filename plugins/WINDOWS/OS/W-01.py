from plugins import Plugin


class windowsosw01(Plugin):
	def __init__(self):
		super().__init__()
		self.code = "W-01"
		self.codeScript = """
echo     ^<infoElement code="%CODE001%"^> >> %RESULT_COLLECT_FILE%

net user Administrator | findstr /bic:"Account active" > administrator_tmp.txt
if "%ERRORLEVEL%" == "0" (
	call :base64encode administrator_tmp.txt
	echo         ^<command name="ADMIN_ACCOUNT"^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
	for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
	echo         ^]^]^>^</command^> >> %RESULT_COLLECT_FILE%
)
if exist administrator_tmp.txt (
	del /q administrator_tmp.txt
)

echo     ^</infoElement^> >> %RESULT_COLLECT_FILE%

secedit /export /cfg secpolicy_tmp.txt > nul
type secpolicy_tmp.txt | more > secpolicy.txt
del /q secpolicy_tmp.txt
if "%ERRORLEVEL%" == "0" (
	call :fileCheckSum secpolicy.txt, checksumvalue
	if not "%checksumvalue%" == "DUP" (
		echo         ^<fileInfo^> >> %RESULT_FILE_DATA_FILE%
		echo             ^<filePath checksum="%checksumvalue%"^>^<!^[CDATA^[Local Security Policy^]^]^>^</filePath^> >> %RESULT_FILE_DATA_FILE%
		call :base64encode secpolicy.txt
		echo             ^<fileData^>^<!^[CDATA^[ >> %RESULT_FILE_DATA_FILE%
		for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_FILE_DATA_FILE%
		echo             ^]^]^>^</fileData^> >> %RESULT_FILE_DATA_FILE%
		echo         ^</fileInfo^> >> %RESULT_FILE_DATA_FILE%  
	)
)
if exist secpolicy.txt (
	del /q secpolicy.txt
)

echo %CODE001% Collect
		"""
		self.codeExcute = "set CODE001=W-01"
		self.description = {
			'Category': '계정 관리',
			'Name': 'Administrator 계정 이름 바꾸기',
			'Important': '상',
			'ImportantScore': '3',
			'Criterion': '양호 : Administrator Default 계정 이름을 변경한 경우\n'
			'취약 : Administrator Default 계정 이름을 변경하지 않은 경우',
			'ActionPlan': 'Administrator Default 계정 이름 변경'
		}
		self.fullString = [self.code, '양호', self.stat, self.description]

	def analysisFunc(self, sysInfo, infoDict, fileDict):
		resultCnt = 0
		activeCnt = 0
		keyList = [
			'CMD:Administrator 계정 활성화 여부(net user)',
			'CMD:Administrator 계정 활성화 여부(Local Security Policy)',
			'CMD:Administrator 계정명 변경 여부(Local Security Policy)'
		]
		if infoDict:
			if 'ADMIN_ACCOUNT' in infoDict[0]:
				activeCnt += self.cmdStrGetValue(keyList[0], infoDict[0], 'ADMIN_ACCOUNT', '^Account active[ \t]*(\\S+)$', 'Yes', 'in')
		else:
			self.stat.update({keyList[0]: f'- Not Found "net user Administrator" Result\n'})
			activeCnt += 1

		fileKey = 'FILEDATA:Local Security Policy'
		if 'Local Security Policy' in fileDict.keys():
			self.stat.update({fileKey: fileDict['Local Security Policy']['fileData']})
			if self.getConfig(fileKey, '^EnableAdminAccount.*$', 'EnableAdminAccount', 'exist'):
				activeCnt += self.compStrValue(fileKey, '^EnableAdminAccount[ \t=]*([0-9])$', '0', 'in')
			self.stat[keyList[1]] = self.stat.pop('FILEDATA:Local Security Policy')

		if activeCnt != 2:
			if 'Local Security Policy' in fileDict.keys():
				self.stat.update({fileKey: fileDict['Local Security Policy']['fileData']})
				if self.getConfig(fileKey, '^NewAdministratorName.*$', 'NewAdministratorName', 'exist'):
					resultCnt += self.compStrValue(fileKey, '^NewAdministratorName[ \t=]*[\"]*([\\S]+[^\"])[\"]*[\\S]$',
					                               'Administrator', '!=')
				self.stat[keyList[2]] = self.stat.pop('FILEDATA:Local Security Policy')
		else:
			resultCnt += 1

		if resultCnt == 0:
			self.fullString[1] = '취약'
		return self.fullString
