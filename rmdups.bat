@echo off
call :sub 1>rmdups.log 2>&1
exit /b
:sub
@echo on
CHCP 65001
echo *** start delete
echo *** end delete