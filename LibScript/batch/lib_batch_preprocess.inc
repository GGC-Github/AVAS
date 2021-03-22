setlocal
chcp 437>nul
PUSHD %~DP0

set DATETEXT=%date:-=%
set hh=%time:~0,2%
set hh1=%hh:~0,1%
set hh2=%hh:~1,1%
if "%hh1%" == " " set hh=0%hh2%
set TIMETEXT=%hh%%time:~3,2%%time:~6,2%
for /f "tokens=*" %%a in ('hostname') do set HOSTNAME=%%a

set RESULT_COLLECT_FILE=result_collect_%HOSTNAME%_%DATETEXT%%TIMETEXT%.xml
set RESULT_FILE_DATA_FILE=result_file_data_%HOSTNAME%_%DATETEXT%%TIMETEXT%.xml

net session > nul 2>&1
if "%ERRORLEVEL%" == "0" goto NEXT
echo.
echo =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
echo.
echo This script must be run as admin.
echo.
echo =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
echo.
pause>nul
exit
:NEXT

set checksumvalue=DUP
