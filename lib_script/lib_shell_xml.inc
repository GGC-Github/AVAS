#############################################################################################
#
# @file lib_shell_xml.inc
# 
# @brief 공통 xml 유틸리티 파일
#
# @version 0.0.1
#
#############################################################################################
xml_file_header_tag() {
	result_file=$1
	echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" > $result_file 2>&1;
}

xml_tag_write() {
	result_file=$1
	write_tag=$2
	depth_space=$3
	write_space=""
	cnt=0
	depth_space=`expr $depth_space '*' 4`
	
	while [ "$cnt" -lt "$depth_space" ]; do
		write_space=`echo "$write_space "`
		cnt=`expr $cnt + 1`
	done

	echo "$write_space$write_tag" >> $result_file 2>&1
}

xml_infoElement_tag_start() {
	code=$1
	echo "    <infoElement code=\"$code\">" >> $RESULT_COLLECT_FILE 2>&1
}

xml_infoElement_tag_end() {
    code=$1
	echo "    </infoElement>" >> $RESULT_COLLECT_FILE 2>&1
	echo "$code Collect"
}

xml_command_write() {
	name=$1
	data=$2
	echo "        <command name=\"$name\"><![CDATA[" >> $RESULT_COLLECT_FILE 2>&1
	enc_data="`(data_cmd_encoding \"$data\")`"
	echo "$enc_data" >> $RESULT_COLLECT_FILE 2>&1
	echo "        ]]></command>" >> $RESULT_COLLECT_FILE 2>&1
}

xml_fileInfo_write() {
	name=$1

	if [ -d "$name" -o -f "$name" ]; then
		chksum=`echo $name | cksum | sed 's/	/ /g' | cut -d ' ' -f1`
		echo "        <fileName><![CDATA[$name]]></fileName>" >> $RESULT_COLLECT_FILE 2>&1

		if [ -z "`cat $RESULT_FILE_DATA_FILE | grep 'checksum=' | awk -F\"=\" '{ print $2 }' | grep \"$chksum\"`" ]; then
			file_stat=`stat -c '%A|%a|%F|%s|%n|%U|%u|%G|%g' $name`
			file_data=`cat "$name" | sed -e 's/^ *//g' -e 's/^	*//g' | egrep -v '^#|^$'`

			echo "        <fileInfo>" >> $RESULT_FILE_DATA_FILE 2>&1
			echo "            <filePath checksum=\"$chksum\"><![CDATA[$name]]></filePath>" >> $RESULT_FILE_DATA_FILE 2>&1
			if [ "$file_stat" != "" ]; then
				echo "            <fileStat><![CDATA[$file_stat]]></fileStat>" >> $RESULT_FILE_DATA_FILE 2>&1
			fi

			if [ -h "$name" ]; then
				if [ "$readlink_cmd" != "" ]; then
					real_name=`$readlink_cmd -f "$name"`
					if [ "$real_name" != "" ]; then
						echo "            <fileRealPath><![CDATA[$real_name]]></fileRealPath>" >> $RESULT_FILE_DATA_FILE 2>&1
						file_realstat=`stat -c '%A|%a|%F|%s|%n|%U|%u|%G|%g' $real_name`
						if [ "$file_realstat" != "" ]; then
							echo "            <fileRealStat><![CDATA[$file_realstat]]></fileRealStat>" >> $RESULT_FILE_DATA_FILE 2>&1
						fi
					fi
				fi
			fi
			echo "            <fileData><![CDATA[" >> $RESULT_FILE_DATA_FILE 2>&1
			if [ "$real_name" != "" ]; then
				enc_data="`(data_file_encoding \"$real_name\")`"
			else
				enc_data="`(data_file_encoding \"$name\")`"
			fi
			echo "$enc_data" >> $RESULT_FILE_DATA_FILE 2>&1
			echo "            ]]></fileData>" >> $RESULT_FILE_DATA_FILE 2>&1
			echo "        </fileInfo>" >> $RESULT_FILE_DATA_FILE 2>&1
		fi
	fi
}

xml_sysInfo_contents() {
	result_file=$1
	OS_TYPE=`uname`
	xml_tag_write "$result_file" "<sysInfo>" "1"
	echo "        <osType>$OS_TYPE</osType>" >> $result_file 2>&1
	case $OS_TYPE in
#		AIX)
#			;;
#		HP-UX)
#			;;
#		SunOS)
#			;;
		Linux)
			OS_KERNEL_VERSION=`uname -r | sed 's/-.*//'`
			if [ -f "/etc/debian_version" -a -f "/etc/lsb-release" ]; then
				OS_VERSION=`cat /etc/debian_version`
				os_chk=`cat /etc/lsb-release | grep "^DISTRIB_ID=" | cut -d '=' -f2 | sed 's/"//g'`
				if [ "$os_chk" = "Ubuntu" ]; then
					OS_VERSION=`cat /etc/lsb-release | grep "^DISTRIB_RELEASE=" | cut -d '=' -f2`
					OS_NAME="Ubuntu"
				fi
			fi

			if [ -f "/etc/redhat-release" ]; then
				OS_NAME_CHK=`cat /etc/redhat-release | grep "CentOS"`
				if [ "$OS_NAME_CHK" != "" ]; then
					OS_NAME="CentOS"
					OS_VERSION=`echo "$OS_NAME_CHK" | sed 's/CentOS //g'`
				fi
			fi
			;;
	esac
	if [ "`command -v base64 2>/dev/null`" != "" ] || [ "`which base64 2>/dev/null`" != "" ]; then
		ENCTYPE="base64"
	fi

    hostname=`hostname`

	echo "        <osName>$OS_NAME</osName>" >> $result_file 2>&1
	echo "        <osVersion>$OS_VERSION</osVersion>" >> $result_file 2>&1
	echo "        <osKernelVersion>$OS_KERNEL_VERSION</osKernelVersion>" >> $result_file 2>&1
	echo "        <hostname>$hostname</hostname>" >> $result_file 2>&1
	echo "        <encType>$ENCTYPE</encType>" >> $result_file 2>&1

    inter_name=`ls /sys/class/net | grep -v 'lo'`
    ip_list=""
    for name in $inter_name; do
        if [ "`command -v ifconfig 2>/dev/null`" != "" ] || [ "`which ifconfig 2>/dev/null`" != "" ]; then
            tmp=`ifconfig $name`
        elif [ "`command -v ip 2>/dev/null`" != "" ] || [ "`which ip 2>/dev/null`" != "" ]; then
            tmp=`ip a show $name`
        fi
        if [ "$ip_list" = "" ]; then
            ip_list=`echo "$tmp"`
        else
            ip_list=`echo -e "$ip_list\n"; echo "$tmp"`
        fi
    done

	process_info=`ps -ef | sed -e 's/^ *//g' -e 's/^	*//g'`
	port_info=`$port_cmd -na | egrep -i 'tcp|udp' | grep -iv 'TIME_WAIT' | sed -e 's/^ *//g' -e 's/^	*//g'`
	if [ "$OS_TYPE" = "Linux" ]; then
	    service_info=`$systemctl_cmd list-units --type service | sed -e 's/^ *//g' -e 's/^	*//g'`
	fi
    if [ "$ip_list" != "" ]; then
        echo "        <ipList><![CDATA[" >> $result_file 2>&1
        enc_ip_list="`(data_cmd_encoding \"$ip_list\")`" >> $result_file 2>&1
        echo "$enc_ip_list" >> $result_file 2>&1
        echo "        ]]></ipList>" >> $result_file 2>&1
    fi
	if [ "$process_info" != "" ]; then
		echo "        <processInfo><![CDATA[" >> $result_file 2>&1
		enc_process_info="`(data_cmd_encoding \"$process_info\")`"
		echo "$enc_process_info" >> $result_file 2>&1
		echo "        ]]></processInfo>" >> $result_file 2>&1
	fi
	if [ "$port_info" != "" ]; then
		echo "        <portInfo><![CDATA[" >> $result_file 2>&1
		enc_port_info="`(data_cmd_encoding \"$port_info\")`"
		echo "$enc_port_info" >> $result_file 2>&1
		echo "        ]]></portInfo>" >> $result_file 2>&1
	fi
	if [ "$service_info" != "" ]; then
		echo "        <serviceInfo><![CDATA[" >> $result_file 2>&1
		enc_service_info="`(data_cmd_encoding \"$service_info\")`"
		echo "$enc_service_info" >> $result_file 2>&1
		echo "        ]]></serviceInfo>" >> $result_file 2>&1
	fi
	xml_tag_write "$result_file" "</sysInfo>" "1"
}
