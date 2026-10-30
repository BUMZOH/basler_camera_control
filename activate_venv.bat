@echo off

cd /d "%~dp0"

call ".venv\Scripts\activate.bat"

doskey p=python $*
doskey pi=python -m pip install $*
doskey pl=python -m pip list

echo.
echo ========================================
echo  Virtual environment activated.
echo.
echo  Aliases:
echo    p  = python
echo    pi = python -m pip install
echo    pl = python -m pip list
echo ========================================
echo.

cmd /k