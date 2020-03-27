#############################################################################################
#
# @file lib_postprocess.inc
# 
# @brief 공통 후작업 유틸리티 파일
#
# @version 0.0.1
#
#############################################################################################

xml_tag_write "$RESULT_COLLECT_FILE" "</infoElementList>" "1"

xml_tag_write "$RESULT_COLLECT_FILE" "<dataElementList>" "1"

xml_tag_write "$RESULT_CMD_DATA_FILE" "</commandList>" "2"

xml_tag_write "$RESULT_FILE_DATA_FILE" "</fileList>" "2"

## Merge Result Files
if [ -f "$RESULT_COLLECT_FILE" ]; then
	if [ -f "$RESULT_CMD_DATA_FILE" ]; then
		cat "$RESULT_CMD_DATA_FILE" >> $RESULT_COLLECT_FILE
		rm -f "$RESULT_CMD_DATA_FILE"
	fi
	if [ -f "$RESULT_FILE_DATA_FILE" ]; then
		cat "$RESULT_FILE_DATA_FILE" >> $RESULT_COLLECT_FILE
		rm -f "$RESULT_FILE_DATA_FILE"
	fi
	xml_tag_write "$RESULT_COLLECT_FILE" "</dataElementList>" "1"
	xml_tag_write "$RESULT_COLLECT_FILE" "</root>" "0"
else
	echo "[Error] Not Found Result Files"
fi
