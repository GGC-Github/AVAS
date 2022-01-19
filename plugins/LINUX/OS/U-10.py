from plugins import Plugin


class linuxosu10(Plugin):
    def __init__(self):
        super().__init__()
        self.code = "U-10"
        self.codeScript = """
linux010() {
    code=$1
    xml_infoElement_tag_start "$code"
    
    xml_fileInfo_write "/etc/xinetd.conf"
    xml_fileInfo_write "/etc/inetd.conf"
    
    if [ -d "/etc/xinetd.d" ]; then
        xinetd_file_list=`ls -d /etc/xinetd.d/* 2>/dev/null`
        for xinetd_file in $xinetd_file_list; do
            xml_fileInfo_write "$xinetd_file"
        done
    fi

    xml_infoElement_tag_end "$code"
}
        """
        self.codeExecute = "linux010 U-10"
        self.description = {
            'Category': '파일 및 디렉터리 관리',
            'Name': '/etc/(x)inetd.conf 파일 소유자 및 권한 설정',
            'Important': '상',
            'ImportantScore': '3',
            'Criterion': '양호 : /etc/(x)inetd.conf 파일의 소유자가 root 이고, 권한이 600인 경우\n'
            '취약 : 양호 : /etc/(x)inetd.conf 파일의 소유자가 root가 아니거나, 권한이 600이 아닌 경우',
            'ActionPlan': '/etc/(x)inetd.conf 파일의 소유자 및 권한 변경(소유자 root, 권한 600)'
        }
        self.fullString = [self.code, '양호', self.stat, self.description]

    def analysisFunc(self, sysInfo, infoDict, fileDict):
        vul_cnt = 0
        if infoDict:
            for file_list in infoDict:
                if file_list in fileDict.keys():
                    reBool = self.filePermCheck(fileDict, file_list, '600', 'root', '<=')
                    if not reBool:
                        vul_cnt += 1
        else:
            self.stat.update({'FILEPERM:/etc/(x)inetd.conf': '- Not Found (x)inetd File\n'})

        if vul_cnt > 0:
            self.fullString[1] = '취약'
        return self.fullString
