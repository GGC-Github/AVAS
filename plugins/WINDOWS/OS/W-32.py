from plugins import Plugin


class windowsosw32(Plugin):
    def __init__(self):
        super().__init__()
        self.code = "W-32"
        self.codeScript = """
call :xml_infoElement_tag_start %CODE032%

wmic qfe list brief /format:texttablewsys | more > hotfix_tmp.txt
if "%ERRORLEVEL%" == "0" call :xml_command_write hotfix_tmp.txt, WINDOWS_HOTFIX
if exist hotfix_tmp.txt del /q hotfix_tmp.txt

reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update" > updatereg_tmp.txt
if "%ERRORLEVEL%" == "0" call :xml_command_write updatereg_tmp.txt, WINDOWS_UPDATE_REG
if exist updatereg_tmp.txt del /q updatereg_tmp.txt

call :xml_infoElement_tag_end %CODE032%
"""
        self.codeExecute = "set CODE032=W-32"
        self.description = {
            'Category': '패치 관리',
            'Name': '최신 HOT FIX 적용',
            'Important': '상',
            'ImportantScore': '3',
            'Criterion': '양호 : 최신 Hotfix가 있는지 주기적으로 모니터링하고 반영하거나, PMS(Patch Management System) Agent가 '
                         '설치되어 자동 패치배포가 적용된 경우\n'
            '취약 : 최신 Hotfix가 있는지 주기적으로 모니터 절차가 없거나, 최신 Hotfix를 반영하지 않은 경우, 또한 PMS(Patch Management System) '
                         'Agent가 설치되어 있지 않거나, 설치되어 있으나 자동 패치배포가 적용되지 않은 경우',
            'ActionPlan': '최신 Hotfix 설치'
        }
        self.fullString = [self.code, '양호', self.stat, self.description]

    def analysisFunc(self, sysInfo, infoDict, fileDict):
        self.fullString[1] = '리뷰'
        keyList = {
            'WINDOWS_HOTFIX': '현재 적용된 패치',
            'WINDOWS_UPDATE_REG': 'update 설정'
        }

        for key in keyList.keys():
            if infoDict:
                for info in infoDict:
                    if key in info:
                        self.stat.update({f'CMD:{keyList[key]}': info[key]})
        return self.fullString
