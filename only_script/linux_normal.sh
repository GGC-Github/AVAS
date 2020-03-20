#!/bin/sh

##### 스크립트 실행 시 언어 설정
lang_check=`locale -a 2>/dev/null | grep "en_US" | egrep -i "(utf8|utf-8)"`
if [ "$lang_check" = "" ]; then
	lang_check="C"
fi

LANG="$lang_check"
LC_ALL="$lang_check"
LANGUAGE="$lang_check"
export LANG
export LC_ALL
export LANGUAGE

##### 포트 명령어 설정
if [ "`command -v netstat 2>/dev/null`" != "" ] || [ "`which netstat 2>/dev/null`" != "" ]; then
	port_cmd="netstat"
else
	port_cmd="ss"
fi

if [ "`command -v systemctl 2>/dev/null`" != "" ] || [ "`which systemctl 2>/dev/null`" != "" ]; then
	systemctl_cmd="systemctl"
fi


##### 수집 파일 지정
RESULT_COLLECT_FILE="Result_Collect_`date +\"%Y%m%d%H%M\"`.txt"
RESULT_VALUE_FILE="Result_Value_`date +\"%Y%m%d%H%M\"`.txt"
##### 시스템 기본 정보 수집
echo "[Start Script]"
echo "====================== Linux Security Check Script Start ======================" >> $RESULT_COLLECT_FILE 2>&1
echo "====================== Linux Security Check Script Start ======================" >> $RESULT_VALUE_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_VALUE_FILE 2>&1

################################################################################################
#
# - 주요 정보 통신 기반 시설 | 계정 관리
# - U-01 root 계정 원격접속 제한
#
################################################################################################

echo "[ U-01 ] : Check"
echo "====================== [U-01 root 계정 원격접속 제한 START]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "1. SSH" >> $RESULT_COLLECT_FILE 2>&1
echo "1-1. SSH Process Check" >> $RESULT_COLLECT_FILE 2>&1
get_ssh_ps=`ps -ef | grep -v "grep" | grep "sshd"`
if [ "$get_ssh_ps" != "" ]; then
	echo "$get_ssh_ps" >> $RESULT_COLLECT_FILE 2>&1
else
	echo "Not Found Process" >> $RESULT_COLLECT_FILE 2>&1
fi
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "1-2. SSH Service Check" >> $RESULT_COLLECT_FILE 2>&1
if [ "$systemctl_cmd" != "" ]; then
	get_ssh_service=`$systemctl_cmd list-units --type service | egrep '(ssh|sshd)\.service' | sed -e 's/^ *//g' -e 's/^	*//g' | tr -s " \t"`
	if [ "$get_ssh_service" != "" ]; then
		echo "$get_ssh_service" >> $RESULT_COLLECT_FILE 2>&1
	else
		echo "Not Found Service" >> $RESULT_COLLECT_FILE 2>&1
	fi
else
	echo "Not Found systemctl Command" >> $RESULT_COLLECT_FILE 2>&1
fi
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "1-3. SSH Port Check" >> $RESULT_COLLECT_FILE 2>&1
if [ "$port_cmd" != "" ]; then
	get_ssh_port=`$port_cmd -na | grep "tcp" | grep "LISTEN" | grep ':22[ \t]'`
	if [ "$get_ssh_port" != "" ]; then
		echo "$get_ssh_port" >> $RESULT_COLLECT_FILE 2>&1
	else
		echo "Not Found Port" >> $RESULT_COLLECT_FILE 2>&1
	fi
else
	echo "Not Found Port Command" >> $RESULT_COLLECT_FILE 2>&1
fi

if [ "$get_ssh_ps" != "" ] || [ "$get_ssh_service" != "" ] || [ "$get_ssh_port" != "" ]; then
	echo "" >> $RESULT_COLLECT_FILE 2>&1
	echo "1-4. SSH Configuration File Check" >> $RESULT_COLLECT_FILE 2>&1
	if [ -f "/etc/ssh/sshd_config" ]; then
		get_ssh_conf=`cat /etc/ssh/sshd_config | egrep -v '^#|^$' | grep "PermitRootLogin"`
		if [ "$get_ssh_conf" != "" ]; then
			echo "/etc/ssh/sshd_config : $get_ssh_conf" >> $RESULT_COLLECT_FILE 2>&1
			get_conf_check=`echo "$get_ssh_conf" | awk '{ print $2 }'`
			if [ "$get_conf_check" = "no" ]; then
				ssh_flag=1
			else
				ssh_flag=0
			fi
		else
			ssh_flag=1
			echo "/etc/ssh/sshd_config : Not Found PermitRootLogin Configuration" >> $RESULT_COLLECT_FILE 2>&1
		fi
	else
		ssh_flag=2
		echo "Not Found SSH Configuration File" >> $RESULT_COLLECT_FILE 2>&1
	fi
	echo "" >> $RESULT_COLLECT_FILE 2>&1
else
	ssh_flag=1
fi

echo "2. Telnet" >> $RESULT_COLLECT_FILE 2>&1
echo "2-1. Telnet Process Check" >> $RESULT_COLLECT_FILE 2>&1
get_telnet_ps=`ps -ef | grep -v "grep" | grep "telnet"`
if [ "$get_telnet_ps" != "" ]; then
	echo "$get_telnet_ps" >> $RESULT_COLLECT_FILE 2>&1
else
	echo "Not Found Process" >> $RESULT_COLLECT_FILE 2>&1
fi
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "2-2. Telnet Service Check" >> $RESULT_COLLECT_FILE 2>&1
if [ "$systemctl_cmd" != "" ]; then
	get_telnet_service=`$systemctl_cmd list-units --type service | egrep '(telnet|telnetd)\.service' | sed -e 's/^ *//g' -e 's/^	*//g' | tr -s " \t"`
	if [ "$get_telnet_service" != "" ]; then
		echo "$get_telnet_service" >> $RESULT_COLLECT_FILE 2>&1
	else
		echo "Not Found Service" >> $RESULT_COLLECT_FILE 2>&1
	fi
else
	echo "Not Found systemctl Command" >> $RESULT_COLLECT_FILE 2>&1
fi
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "2-3. Telnet Port Check" >> $RESULT_COLLECT_FILE 2>&1
if [ "$port_cmd" != "" ]; then
	get_telnet_port=`$port_cmd -na | grep "tcp" | grep "LISTEN" | grep ':23[ \t]'`
	if [ "$get_telnet_port" != "" ]; then
		echo "$get_telnet_port" >> $RESULT_COLLECT_FILE 2>&1
	else
		echo "Not Found Port" >> $RESULT_COLLECT_FILE 2>&1
	fi
else
	echo "Not Found Port Command" >> $RESULT_COLLECT_FILE 2>&1
fi

if [ "$get_telnet_ps" != "" ] || [ "$get_telnet_service" != "" ] || [ "$get_telnet_port" != "" ]; then
	echo "" >> $RESULT_COLLECT_FILE 2>&1
	echo "2.4 Telnet Configuration Check" >> $RESULT_COLLECT_FILE 2>&1
	if [ -f "/etc/pam.d/remote" ]; then
		pam_file="/etc/pam.d/remote"
	elif [ -f "/etc/pam.d/login" ]; then
		pam_file="/etc/pam.d/login"
	fi

	if [ "$pam_file" != "" ]; then
		echo "- $pam_file" >> $RESULT_COLLECT_FILE 2>&1
		get_conf=`cat $pam_file | egrep -v '^#|^$' | grep "pam_securetty.so"`
		if [ "$get_conf" != "" ]; then
			echo "$get_conf" >> $RESULT_COLLECT_FILE 2>&1
			if [ -f "/etc/securetty" ]; then
				echo "- /etc/securetty" >> $RESULT_COLLECT_FILE 2>&1
				get_pts=`cat /etc/securetty | egrep -v '^#|^$' | grep "^[ \t]*pts"` >> $RESULT_COLLECT_FILE 2>&1
				if [ "$get_pts" != "" ]; then
					telnet_flag=0
				else
					telnet_flag=1
				fi
			else
				telnet_flag=0
				echo "Not Found Telnet tty Configuration File" >> $RESULT_COLLECT_FILE 2>&1
			fi
		else
			telnet_flag=0
			echo "$pam_file : Not Found pam_securetty.so Configuration" >> $RESULT_COLLECT_FILE 2>&1
		fi
	else
		telnet_flag=2
		echo "Not Found Telnet Pam Configuration File" >> $RESULT_COLLECT_FILE 2>&1
	fi
else
	telnet_flag=1
fi

# 양호 : 1, 취약 : 0, 검토 : 2
if [ $ssh_flag -eq 1 ] && [ $telnet_flag -eq 1 ]; then
	echo "[ U-01 ] : 양호" >> $RESULT_VALUE_FILE 2>&1
elif [ $ssh_flag -eq 0 ] || [ $telnet_flag -eq 0 ]; then
	echo "[ U-01 ] : 취약" >> $RESULT_VALUE_FILE 2>&1
elif [ $ssh_flag -eq 2 ] || [ $telnet_flag -eq 2 ]; then
	echo "[ U-01 ] : 검토" >> $RESULT_VALUE_FILE 2>&1
fi

echo "" >> $RESULT_COLLECT_FILE 2>&1
echo "====================== [U-01 root 계정 원격접속 제한 END]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

################################################################################################
#
# - 주요 정보 통신 기반 시설 | 계정 관리
# - U-03 계정 잠금 임계값 설정
#
################################################################################################

echo "[ U-03 ] : Check"
echo "====================== [U-03 계정 잠금 임계값 설정 START]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

retries_path="/etc/pam.d/system-auth /etc/pam.d/password-auth /etc/pam.d/common-auth /etc/pam.d/common-account"
get_deny_count=0
for file in $retries_path; do
	echo "- $file" >> $RESULT_COLLECT_FILE 2>&1
	if [ -f "$file" ]; then
		get_deny=`cat "$file" | grep -v '^#'  | grep 'pam_tally' | egrep 'deny|lock_time'`
		if [ "$get_deny" != "" ]; then
			echo "$get_deny" >> $RESULT_COLLECT_FILE 2>&1
			get_deny_count=`expr $get_deny_count + 1`
		else
			echo "Not Found Retries & Lock Time" >> $RESULT_COLLECT_FILE 2>&1
		fi
	else
		echo "Not Found Configuration File" >> $RESULT_COLLECT_FILE 2>&1
	fi
	echo "" >> $RESULT_COLLECT_FILE 2>&1
done

if [ "$get_deny_count" -gt 0 ]; then
	echo "[ U-03 ] : 양호" >> $RESULT_VALUE_FILE 2>&1
else
	echo "[ U-03 ] : 취약" >> $RESULT_VALUE_FILE 2>&1
fi

echo "====================== [U-03 계정 잠금 임계값 설정 END]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

################################################################################################
#
# - 주요 정보 통신 기반 시설 | 파일 및 디렉터리 관리
# - U-07 /etc/passwd 파일 소유자 및 권한 설정
#
################################################################################################

echo "[ U-07 ] : Check"
echo "====================== [U-07 /etc/passwd 파일 소유자 및 권한 설정 START]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

if [ -f "/etc/passwd" ]; then
	ls -l /etc/passwd >> $RESULT_COLLECT_FILE 2>&1
	permission_val=`stat -c '%a' /etc/passwd`
	owner_val=`stat -c '%U' /etc/passwd`

	owner_perm_val=`echo "$permission_val" | awk '{ print substr($0, 1, 1) }'`
	group_perm_val=`echo "$permission_val" | awk '{ print substr($0, 2, 1) }'`
	other_perm_val=`echo "$permission_val" | awk '{ print substr($0, 3, 1) }'`

	if [ "$owner_perm_val" -le 6 ] && [ "$group_perm_val" -le 4 ] && [ "$other_perm_val" -le 4 ] && [ "$owner_val" = "root" ]; then
		echo "[ U-07 ] : 양호" >> $RESULT_VALUE_FILE 2>&1
	else
		echo "[ U-07 ] : 취약" >> $RESULT_VALUE_FILE 2>&1
	fi
else
	echo "Not Found /etc/passwd File" >> $RESULT_COLLECT_FILE 2>&1
	echo "[ U-07 ] : 검토" >> $RESULT_VALUE_FILE 2>&1
fi

echo "" >> $RESULT_COLLECT_FILE 2>&1
echo "====================== [U-07 /etc/passwd 파일 소유자 및 권한 설정 END]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

################################################################################################
#
# - 주요 정보 통신 기반 시설 | 파일 및 디렉터리 관리
# - U-08 /etc/shadow 파일 소유자 및 권한 설정
#
################################################################################################

echo "[ U-08 ] : Check"
echo "====================== [U-08 /etc/shadow 파일 소유자 및 권한 설정 START]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

if [ -f "/etc/shadow" ]; then
	ls -l /etc/shadow >> $RESULT_COLLECT_FILE 2>&1
	permission_val=`stat -c '%a' /etc/shadow`
	owner_val=`stat -c '%U' /etc/shadow`

	if [ "$permission_val" -eq 0 ]; then
		permission_val="000"
	fi

	owner_perm_val=`echo "$permission_val" | awk '{ print substr($0, 1, 1) }'`
	group_perm_val=`echo "$permission_val" | awk '{ print substr($0, 2, 1) }'`
	other_perm_val=`echo "$permission_val" | awk '{ print substr($0, 3, 1) }'`

	if [ "$owner_perm_val" -le 6 ] && [ "$group_perm_val" -eq 0 ] && [ "$other_perm_val" -eq 0 ] && [ "$owner_val" = "root" ]; then
		echo "[ U-08 ] : 양호" >> $RESULT_VALUE_FILE 2>&1
	else
		echo "[ U-08 ] : 취약" >> $RESULT_VALUE_FILE 2>&1
	fi
else
	echo "Not Found /etc/shadow File" >> $RESULT_COLLECT_FILE 2>&1
	echo "[ U-08 ] : 검토" >> $RESULT_VALUE_FILE 2>&1
fi

echo "" >> $RESULT_COLLECT_FILE 2>&1
echo "====================== [U-08 /etc/shadow 파일 소유자 및 권한 설정 END]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

################################################################################################
#
# - 주요 정보 통신 기반 시설 | 서비스 관리
# - U-31 스팸 메일 릴레이 제한
#
################################################################################################

echo "[ U-31 ] : Check"
echo "====================== [U-31 스팸 메일 릴레이 제한 START]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "1. Sendmail Process Check" >> $RESULT_COLLECT_FILE 2>&1
get_sendmail_ps=`ps -ef | grep -v "grep" | grep "sendmail"`
if [ "$get_sendmail_ps" != "" ]; then
	echo "$get_sendmail_ps" >> $RESULT_COLLECT_FILE 2>&1
else
	echo "Not Found Process" >> $RESULT_COLLECT_FILE 2>&1
fi
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "2. Sendmail Service Check" >> $RESULT_COLLECT_FILE 2>&1
if [ "$systemctl_cmd" != "" ]; then
	get_sendmail_service=`$systemctl_cmd list-units --type service | grep 'sendmail\.service' | sed -e 's/^ *//g' -e 's/^	*//g' | tr -s " \t"`
	if [ "$get_sendmail_service" != "" ]; then
		echo "$get_sendmail_service" >> $RESULT_COLLECT_FILE 2>&1
	else
		echo "Not Found Service" >> $RESULT_COLLECT_FILE 2>&1
	fi
else
	echo "Not Found systemctl Command" >> $RESULT_COLLECT_FILE 2>&1
fi

if [ "$get_sendmail_ps" != "" ] || [ "$get_sendmail_service" != "" ]; then
	echo "" >> $RESULT_COLLECT_FILE 2>&1
	echo "3. Sendmail Configuration Check" >> $RESULT_COLLECT_FILE 2>&1

	if [ -f "/etc/mail/sendmail.cf" ]; then
		sendmail_file="/etc/mail/sendmail.cf"
	elif [ -f "/etc/sendmail.cf" ]; then
		sendmail_file="/etc/sendmail.cf"
	fi

	if [ "$sendmail_file" != "" ]; then
		echo "- $sendmail_file" >> $RESULT_COLLECT_FILE 2>&1
		get_sendmail_conf=`cat "$sendmail_file" | egrep -v '^#|^$' | egrep -i "R$\*|Relaying\sdenied"`
		if [ "$get_sendmail_conf" != "" ]; then
			echo "$get_sendmail_conf" >> $RESULT_COLLECT_FILE 2>&1
			echo "[ U-31 ] : 양호" >> $RESULT_VALUE_FILE 2>&1
		else
			echo "Not Found Spam Relay Configuration" >> $RESULT_COLLECT_FILE 2>&1
			echo "[ U-31 ] : 취약" >> $RESULT_VALUE_FILE 2>&1
		fi
	else
		echo "Not Found Sendmail Configuration File" >> $RESULT_COLLECT_FILE 2>&1
	fi
fi

echo "" >> $RESULT_COLLECT_FILE 2>&1
echo "====================== [U-31 스팸 메일 릴레이 제한 END]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

################################################################################################
#
# - 주요 정보 통신 기반 시설 | 서비스 관리
# - U-32 일반 사용자의 Sendmail 실행 방지
#
################################################################################################

echo "[ U-32 ] : Check"
echo "====================== [U-32 일반 사용자의 Sendmail 실행 방지 START]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "1. Sendmail Process Check" >> $RESULT_COLLECT_FILE 2>&1
get_sendmail_ps=`ps -ef | grep -v "grep" | grep "sendmail"`
if [ "$get_sendmail_ps" != "" ]; then
	echo "$get_sendmail_ps" >> $RESULT_COLLECT_FILE 2>&1
else
	echo "Not Found Process" >> $RESULT_COLLECT_FILE 2>&1
fi
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "2. Sendmail Service Check" >> $RESULT_COLLECT_FILE 2>&1
if [ "$systemctl_cmd" != "" ]; then
	get_sendmail_service=`$systemctl_cmd list-units --type service | grep 'sendmail\.service' | sed -e 's/^ *//g' -e 's/^	*//g' | tr -s " \t"`
	if [ "$get_sendmail_service" != "" ]; then
		echo "$get_sendmail_service" >> $RESULT_COLLECT_FILE 2>&1
	else
		echo "Not Found Service" >> $RESULT_COLLECT_FILE 2>&1
	fi
else
	echo "Not Found systemctl Command" >> $RESULT_COLLECT_FILE 2>&1
fi

if [ "$get_sendmail_ps" != "" ] || [ "$get_sendmail_service" != "" ]; then
	echo "" >> $RESULT_COLLECT_FILE 2>&1
	echo "3. Sendmail Configuration Check" >> $RESULT_COLLECT_FILE 2>&1

	if [ -f "/etc/mail/sendmail.cf" ]; then
		sendmail_file="/etc/mail/sendmail.cf"
	elif [ -f "/etc/sendmail.cf" ]; then
		sendmail_file="/etc/sendmail.cf"
	fi

	if [ "$sendmail_file" != "" ]; then
		echo "- $sendmail_file" >> $RESULT_COLLECT_FILE 2>&1
		get_sendmail_conf=`cat "$sendmail_file" | egrep -v '^#|^$' | grep -i "PrivacyOptions" | grep -i "restrictqrun"`
		if [ "$get_sendmail_conf" != "" ]; then
			echo "$get_sendmail_conf" >> $RESULT_COLLECT_FILE 2>&1
			echo "[ U-32 ] : 양호" >> $RESULT_VALUE_FILE 2>&1
		else
			echo "Not Found PrivacyOptions restrictqrun Configuration" >> $RESULT_COLLECT_FILE 2>&1
			echo "[ U-32 ] : 취약" >> $RESULT_VALUE_FILE 2>&1
		fi
	else
		echo "Not Found Sendmail Configuration File" >> $RESULT_COLLECT_FILE 2>&1
	fi
fi

echo "" >> $RESULT_COLLECT_FILE 2>&1
echo "====================== [U-32 일반 사용자의 Sendmail 실행 방지 END]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

################################################################################################
#
# - 주요 정보 통신 기반 시설 | 패치 관리
# - U-42 최신 보안패치 및 벤더 권고사항 적용
#
################################################################################################

echo "[ U-42 ] : Check"
echo "====================== [U-42 최신 보안패치 및 벤더 권고사항 적용 START]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "[ U-42 ] : 검토" >> $RESULT_VALUE_FILE 2>&1
OS_KERNEL_VERSION=`uname -r`
echo "1. OS 커널 버전" >> $RESULT_COLLECT_FILE 2>&1
if [ "$OS_KERNEL_VERSION" != "" ]; then
	echo "- $OS_KERNEL_VERSION" >> $RESULT_COLLECT_FILE 2>&1
else
	echo "- Not Found OS Kernel Version" >> $RESULT_COLLECT_FILE 2>&1
fi

echo "" >> $RESULT_COLLECT_FILE 2>&1
echo "2. OS 버전" >> $RESULT_COLLECT_FILE 2>&1
if [ -f "/etc/debian_version" -a -f "/etc/lsb-release" ]; then
	OS_VERSION=`cat /etc/lsb-release | grep "^DISTRIB_RELEASE" | cut -d '=' -f2`
	if [ "$OS_VERSION" != "" ]; then
		OS_FULL_VERSION="Ubuntu $OS_VERSION"
		echo "- $OS_FULL_VERSION" >> $RESULT_COLLECT_FILE 2>&1
	else
		echo "- Not Found OS Version" >> $RESULT_COLLECT_FILE 2>&1
	fi
elif [ -f "/etc/redhat-release" ]; then
	OS_FULL_VERSION=`cat /etc/redhat-release | grep "CentOS"`
	if [ "$OS_FULL_VERSION" != "" ]; then
		echo "- $OS_FULL_VERSION" >> $RESULT_COLLECT_FILE 2>&1
	else
		echo "- Not Found OS Version" >> $RESULT_COLLECT_FILE 2>&1
	fi
else
	echo "- Not Found OS Version" >> $RESULT_COLLECT_FILE 2>&1
fi

echo "" >> $RESULT_COLLECT_FILE 2>&1
echo "====================== [U-42 최신 보안패치 및 벤더 권고사항 적용 END]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

################################################################################################
#
# - 주요 정보 통신 기반 시설 | 로그 관리
# - U-43 로그의 정기적 검토 및 보고
#
################################################################################################

echo "[ U-43 ] : Check"
echo "====================== [U-43 로그의 정기적 검토 및 보고 START]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "Step 1) 정기적인 로그 검토 및 분석 주기 수립" >> $RESULT_COLLECT_FILE 2>&1
echo "1. utmp, wtmp, btmp 등의 로그를 확인하여 마지막 로그인 시간, 접속 IP, 실패한 이력 등을 확인하여 계정 탈취 공격 및 시스템 해킹 여보를 검토" >> $RESULT_COLLECT_FILE 2>&1
echo "2. sulog를 확인하여 허용된 계정 외에 su 명령어를 통해 권한 상승을 시도하였는지 검토" >> $RESULT_COLLECT_FILE 2>&1
echo "3. xferlog를 확인하여 비인가자의 ftp 접근 여부를 검토" >> $RESULT_COLLECT_FILE 2>&1
echo "Step 2) 로그 분석에 대한 결과 보고서 작성" >> $RESULT_COLLECT_FILE 2>&1
echo "Step 3) 로그 분석 결과보고서 보고 체계 수립" >> $RESULT_COLLECT_FILE 2>&1
echo "[ U-43 ] : 검토" >> $RESULT_VALUE_FILE 2>&1

echo "" >> $RESULT_COLLECT_FILE 2>&1
echo "====================== [U-43 로그의 정기적 검토 및 보고 END]" >> $RESULT_COLLECT_FILE 2>&1
echo "" >> $RESULT_COLLECT_FILE 2>&1

echo "" >> $RESULT_VALUE_FILE 2>&1
echo "======================= Linux Security Check Script End =======================" >> $RESULT_COLLECT_FILE 2>&1
echo "======================= Linux Security Check Script End =======================" >> $RESULT_VALUE_FILE 2>&1
echo "[End Script]"
