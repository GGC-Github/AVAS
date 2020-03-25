#############################################################################################
#
# @file lib_xml.inc
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

xml_root_tag_start() {
	result_file=$1
	echo "<root>" >> $result_file 2>&1;
}

xml_root_tag_end() {
	result_file=$1
	echo "</root>" >> $result_file 2>&1;
}

xml_sysInfo_tag_start() {
	result_file=$1
	echo "    <sysInfo>" >> $result_file 2>&1
}

xml_sysInfo_tag_end() {
	result_file=$1
	echo "    </sysInfo>" >> $result_file 2>&1
}

xml_infoElementList_tag_start() {
	result_file=$1
	echo "    <infoElementList>" >> $result_file 2>&1
}

xml_infoElementList_tag_end() {
	result_file=$1
	echo "    </infoElementList>" >> $result_file 2>&1
}

xml_dataElementList_tag_start() {
	result_file=$1
	echo "    <dataElementList>" >> $result_file 2>&1
}

xml_dataElementList_tag_end() {
	result_file=$1
	echo "    </dataElementList>" >> $result_file 2>&1
}

xml_commandList_tag_start() {
	result_file=$1
	echo "        <commandList>" > $result_file 2>&1
}

xml_commandList_tag_end() {
	result_file=$1
	echo "        </commandList>" >> $result_file 2>&1
}

xml_fileList_tag_start() {
	result_file=$1
	echo "        <fileList>" > $result_file 2>&1
}

xml_fileList_tag_end() {
	result_file=$1
	echo "        </fileList>" >> $result_file 2>&1
}

xml_infoElement_tag_start() {
	code=$1
	echo "        <infoElement code=\"$code\">" >> $RESULT_COLLECT_FILE 2>&1
	echo "            <commandCode code=\"$code\">" >> $RESULT_CMD_DATA_FILE 2>&1
}

xml_infoElement_tag_end() {
	echo "        </infoElement>" >> $RESULT_COLLECT_FILE 2>&1
	echo "            </commandCode>" >> $RESULT_CMD_DATA_FILE 2>&1
}

xml_colInfoList_tag_start() {
	echo "            <colInfoList>" >> $RESULT_COLLECT_FILE 2>&1
}

xml_colInfoList_tag_end() {
	echo "            </colInfoList>" >> $RESULT_COLLECT_FILE 2>&1
}

xml_command_write() {
	name=$1
	data=$2
	enc_data="$data"
	echo "                <command><![CDATA[$name]]></command>" >> $RESULT_COLLECT_FILE 2>&1
	echo "                <commandElement name=\"$name\"><![CDATA[" >> $RESULT_CMD_DATA_FILE 2>&1
	echo "$enc_data" >> $RESULT_CMD_DATA_FILE 2>&1
	echo "                ]]></commandElement>" >> $RESULT_CMD_DATA_FILE 2>&1
}

xml_fileInfo_write() {
	name=$1
	contents_flag=0
	if [ "$2" = "contents" ]; then
		contents_flag=1
	fi

	if [ -d "$name" -o -f "$name" ]; then
		file_stat=`ls -al $name`
		file_data=`cat "$name" | sed -e 's/^ *//g' -e 's/^	*//g' | egrep -v '^#|^$'`

		echo "                <fileName><![CDATA[$name]]></fileName>" >> $RESULT_COLLECT_FILE 2>&1

		echo "            <fileInfo>" >> $RESULT_FILE_DATA_FILE 2>&1
		echo "                <filePath><![CDATA[$name]]></filePath>" >> $RESULT_FILE_DATA_FILE 2>&1
		echo "                <fileStat><![CDATA[$file_stat]]></fileStat>" >> $RESULT_FILE_DATA_FILE 2>&1
		echo "                <fileData><![CDATA[" >> $RESULT_FILE_DATA_FILE 2>&1
		echo "$file_data" >> $RESULT_FILE_DATA_FILE 2>&1
		echo "                ]]></fileData>" >> $RESULT_FILE_DATA_FILE 2>&1
		echo "            </fileInfo>" >> $RESULT_FILE_DATA_FILE 2>&1
	fi
}

xml_sysInfo_contents() {
	result_file=$1
	OS_TYPE=`uname`
	xml_sysInfo_tag_start "$result_file"
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
	process_info=`ps -ef`
	port_info=`$port_cmd -na | egrep -i 'tcp|udp' | grep -iv 'TIME_WAIT'`
	echo "        <osName>$OS_NAME</osName>" >> $result_file 2>&1
	echo "        <osVersion>$OS_VERSION</osVersion>" >> $result_file 2>&1
	echo "        <osKernelVersion>$OS_KERNEL_VERSION</osKernelVersion>" >> $result_file 2>&1
	if [ "$process_info" != "" ]; then
		echo "        <processInfo><![CDATA[" >> $result_file 2>&1
		echo "$process_info" >> $result_file 2>&1
		echo "        ]]></processInfo>" >> $result_file 2>&1
	fi
	if [ "$port_info" != "" ]; then
		echo "        <portInfo><![CDATA[" >> $result_file 2>&1
		echo "$port_info" >> $result_file 2>&1
		echo "        ]]></portInfo>" >> $result_file 2>&1
	fi
	xml_sysInfo_tag_end "$result_file"
}

xml_file_header_tag "$RESULT_COLLECT_FILE"
xml_root_tag_start "$RESULT_COLLECT_FILE"
xml_sysInfo_contents "$RESULT_COLLECT_FILE"
xml_infoElementList_tag_start "$RESULT_COLLECT_FILE"

xml_commandList_tag_start "$RESULT_CMD_DATA_FILE"
xml_fileList_tag_start "$RESULT_FILE_DATA_FILE"
