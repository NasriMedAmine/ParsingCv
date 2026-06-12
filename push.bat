@echo off
title Git Auto Push

echo =========================
echo      Git Auto Push
echo =========================
echo.

set /p msg=Commit message: 

git add .

git commit -m "%msg%"

git push origin main

echo.
echo =========================
echo        Finished
echo =========================
pause