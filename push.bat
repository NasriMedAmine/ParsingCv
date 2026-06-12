@echo off
title Git Auto Push

echo =========================
echo      Git Auto Push
echo =========================
echo.

set /p msg=Commit message: 

git add .
git remote add origin https://github.com/NasriMedAmine/ParsingCv.git
git branch -M main
git commit -m "%msg%"

git push origin main

echo.
echo =========================
echo        Finished
echo =========================
pause