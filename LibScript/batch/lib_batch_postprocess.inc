:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: @file lib_batch_postprocess.inc
::
:: @brief 공통 후작업 유틸리티 파일
::
:: @version 0.0.1
::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

echo     ^</fileList^> >> %RESULT_FILE_DATA_FILE%
copy %RESULT_COLLECT_FILE% + %RESULT_FILE_DATA_FILE% %RESULT_COLLECT_FILE% /b
echo ^</root^> >> %RESULT_COLLECT_FILE%

del /q "systeminfo.txt"
del /q "base64.txt"
del /q "filecksum.txt"
del /q "%RESULT_FILE_DATA_FILE%"

exit /b 0
:base64encode
	certutil -encode %~1 base64tmp.txt > nul
	type base64tmp.txt | findstr /v CERTIFICATE > base64.txt
	del /q %~1
	del /q base64tmp.txt
exit /b

:fileCheckSum
    certutil -hashfile %~1 > filecksumtmp.txt
    for /f "tokens=*" %%a in ('"type filecksumtmp.txt | findstr /v "%~1 hash""') do set chksumvalue=%%a
    set chksumvalue=%chksumvalue: =%
    if exist filecksum.txt (
        type filecksum.txt | findstr /bic:%chksumvalue% > nul
        if "%ERRORLEVEL%" == "0" (
            set %~2=DUP
        ) else (
            echo %chksumvalue% >> filecksum.txt
            set %~2=%chksumvalue%
        )
    ) else (
        echo %chksumvalue% > filecksum.txt
        set %~2=%chksumvalue%
    )
    del /q filecksumtmp.txt
exit /b