from plugins import Plugin


class linuxosu04(Plugin):
    def __init__(self):
        super().__init__()
        self.code = "U-04"
        self.codeScript = """
linux004() {
    code=$1
    xml_infoElement_tag_start "$code"

    xml_fileInfo_write "/etc/passwd"
    xml_fileInfo_write "/etc/shadow"

    xml_infoElement_tag_end "$code"
}
        """
        self.codeExecute = "linux004 U-04"
        self.description = {
            'Category': '계정 관리',
            'Name': '패스워드 파일 보호',
            'Important': '상',
            'ImportantScore': '3',
            'Criterion': '양호 : 쉐도우 패스워드를 사용하거나, 패스워드를 암호화하여 저장하는 경우\n'
            '취약 : 쉐도우 패스워드를 사용하지 않고, 패스워드를 암호화하여 저장하지 않는 경우',
            'ActionPlan': '패스워드 암호화 저장·관리 설정 적용'
        }
        self.fullString = [self.code, '양호', self.stat, self.description]

    def analysisFunc(self, sysInfo, infoDict, fileDict):
        shadow_flag = False
        enc_type_dict = {1: "MD5", 5: "SHA-256", 6: "SHA-512"}
        enc_type = ""
        if "/etc/passwd" in infoDict:
            lines = [data for data in fileDict["/etc/passwd"]["fileData"].splitlines() if "$" in data.split(":")[1]]
            if not lines:
                if "/etc/shadow" in infoDict:
                    shadow_flag = True
                    lines = [data for data in fileDict["/etc/shadow"]["fileData"].splitlines() if "$" in data.split(":")[1]]
                    if int(f"{lines}".split(":")[1].split("$")[1]) in enc_type_dict.keys():
                        enc_type = f"{lines}".split(":")[1].split("$")[1]
            else:
                if int(f"{lines}".split(":")[1].split("$")[1]) in enc_type_dict.keys():
                    enc_type = f"{lines}".split(":")[1].split("$")[1]
            if not enc_type:
                self.stat.update({"ㅁ Encryption Type": f"Not Found Encryption Type (!)\n"})
                self.fullString[1] = "취약"
            elif int(enc_type) in enc_type_dict.keys():
                if 5 > int(enc_type):
                    self.stat.update({"ㅁ Encryption Type": f"{enc_type_dict[int(enc_type)]} (Low Security Strength) (!)\n"})
                    self.fullString[1] = "취약"
                else:
                    self.stat.update({"ㅁ Encryption Type": f"{enc_type_dict[int(enc_type)]}\n"})
            self.stat.update({"FILEDATA:/etc/passwd": fileDict["/etc/passwd"]["fileData"]})
            if shadow_flag:
                self.stat.update({"FILEDATA:/etc/shadow": fileDict["/etc/shadow"]["fileData"]})
            else:
                self.stat.update({"FILEDATA:/etc/shadow": "Not Found /etc/shadow File (!)\n"})
                self.fullString[1] = "취약"
        else:
            self.stat.update({"FILEDATA:/etc/passwd": "Not Found /etc/passwd File\n"})
        return self.fullString
