from plugins import Plugin


class linuxosu09(Plugin):
    def __init__(self):
        super().__init__()
        self.code = "U-09"
        self.codeScript = """
linux009() {
    code=$1
    xml_infoElement_tag_start "$code"

    xml_fileInfo_write "/etc/hosts"

    xml_infoElement_tag_end "$code"
}
        """
        self.codeExecute = "linux009 U-09"
        self.description = {
            'Category': '파일 및 디렉터리 관리',
            'Name': '/etc/hosts 파일 소유자 및 권한 설정',
            'Important': '상',
            'ImportantScore': '3',
            'Criterion': '양호 : /etc/hosts 파일의 소유자가 root 이고, 권한이 600 이하인 경우\n'
            '취약 : /etc/hosts 파일의 소유자가 root가 아니거나 권한이 600 초과인 경우',
            'ActionPlan': '/etc/hosts 파일의 소유자 및 권한 변경(소유자 root, 권한 600)'
        }
        self.fullString = [self.code, '양호', self.stat, self.description]

    def analysisFunc(self, sysInfo, infoDict, fileDict):
        reBool = True
        if '/etc/hosts' in fileDict.keys():
            reBool = self.filePermCheck(fileDict, '/etc/hosts', '600', 'root', '<=')
        else:
            self.stat.update({'FILEPERM:/etc/hosts': '- Not Found /etc/hosts File\n'})

        if not reBool:
            self.fullString[1] = '취약'
        return self.fullString
