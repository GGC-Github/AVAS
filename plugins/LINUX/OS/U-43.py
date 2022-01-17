from plugins import Plugin


class linuxosu43(Plugin):
    def __init__(self):
        super().__init__()
        self.code = "U-43"
        self.codeScript = """
linux043() {
    code=$1
    xml_infoElement_tag_start "$code"

    xml_infoElement_tag_end "$code"
}
        """
        self.codeExecute = "linux043 U-43"
        self.description = {
            'Category': '로그 관리',
            'Name': '로그의 정기적 검토 및 보고',
            'Important': '상',
            'ImportantScore': '3',
            'Criterion': '양호 : 로그 기록의 검토, 분석, 리포트 작성 및 보고 등이 정기적으로 이루어지는 경우\n'
            '취약 : 로그 기록의 검토, 분석, 리포트 작성 및 보고 등이 정기적으로 이루어지지 않는 경우',
            'ActionPlan': '로그 기록 검토 및 분석을 시행하여 리포트를 작성하고 정기적으로 보고함'
        }
        self.fullString = [self.code, '양호', self.stat, self.description]

    def analysisFunc(self, sysInfo, infoDict, fileDict):
        reviewStr = """
Step 1) 정기적인 로그 검토 및 분석 주기 수립
    1. utmp, wtmp, btmp 등의 로그를 확인하여 마지막 로그인 시간, 접속 IP, 실패한 이력 등을 확인하여 계정 탈취 공격 및 시스템 해킹 여부를 검토
    2. sulog를 확인하여 허용된 계정 외에 su 명령어를 통해 권한상승을 시도하였는지 검토
    3. xferlog를 확인하여 비인가자의 ftp 접근 여부를 검토
Step 2) 로그 분석에 대한 결과 보고서 작성
Step 3) 로그 분석 결과보고서 보고 체계 수립        
        """
        self.stat.update({'CMD:정기적인 로그 분석을 위하여 아래와 같은 절차 수립': reviewStr})
        self.fullString[1] = '리뷰'
        return self.fullString
