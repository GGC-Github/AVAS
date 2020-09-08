echo ^<?xml version="1.0" encoding="UTF-8"?^> > %RESULT_COLLECT_FILE%
echo ^<root^> >> %RESULT_COLLECT_FILE%
echo     ^<assetInfo^> >> %RESULT_COLLECT_FILE%
echo         ^<assetType^>%ASSETTYPE%^</assetType^> >> %RESULT_COLLECT_FILE%
echo         ^<assetSubType^>%ASSETSUBTYPE%^</assetSubType^> >> %RESULT_COLLECT_FILE%
echo     ^</assetInfo^> >> %RESULT_COLLECT_FILE%
echo     ^<sysInfo^> >> %RESULT_COLLECT_FILE%

systeminfo > systeminfo.txt
for /f "tokens=1,2 delims=:" %%a in ('"findstr /bic:"OS Name" systeminfo.txt"') do set OSNAME=%%b
for /f "tokens=1,2 delims=:" %%a in ('"findstr /bic:"OS Version" systeminfo.txt"') do set OSVERSION=%%b
for /f "tokens=1,2 delims=:" %%a in ('"findstr /bic:"OS Host Name" systeminfo.txt"') do set HOSTNAME=%%b

set OSNAME=%OSNAME: =%
set OSVERSION=%OSVERSION: =%
set HOSTNAME=%HOSTNAME: =%

echo         ^<osType^>Windows^</osType^> >> %RESULT_COLLECT_FILE%
echo         ^<osName^>%OSNAME%^</osName^> >> %RESULT_COLLECT_FILE%
echo         ^<osVersion^>%OSVERSION%^</osVersion^> >> %RESULT_COLLECT_FILE%
echo         ^<hostname^>%HOSTNAME%^</hostname^> >> %RESULT_COLLECT_FILE%

certutil > nul
if "%ERRORLEVEL%" == "0" (set ENCTYPE=base64) else (set ENCTYPE=NULL)
echo         ^<encType^>%ENCTYPE%^</encType^> >> %RESULT_COLLECT_FILE%

ipconfig | more > iplist.txt
call :base64encode iplist.txt
echo         ^<ipList^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
echo         ^]^]^>^</ipList^> >> %RESULT_COLLECT_FILE%

tasklist | more > tasklist.txt
call :base64encode tasklist.txt
echo         ^<processInfo^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
echo         ^]^]^>^</processInfo^> >> %RESULT_COLLECT_FILE%

netstat -ano | more > portlist.txt
call :base64encode portlist.txt
echo         ^<portInfo^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
echo         ^]^]^>^</portInfo^> >> %RESULT_COLLECT_FILE%

net start | more > servicelist.txt
call :base64encode servicelist.txt
echo         ^<serviceInfo^>^<!^[CDATA^[ >> %RESULT_COLLECT_FILE%
for /f "delims=" %%a in (base64.txt) do echo %%a >> %RESULT_COLLECT_FILE%
echo         ^]^]^>^</serviceInfo^> >> %RESULT_COLLECT_FILE%

echo     ^</sysInfo^> >> %RESULT_COLLECT_FILE%

echo     ^<fileList^> > %RESULT_FILE_DATA_FILE%
