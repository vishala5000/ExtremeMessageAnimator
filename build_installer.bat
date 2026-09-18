@echo off

echo ==========================================
echo EXTREME MESSAGE ANIMATOR
echo WINDOWS BUILD
echo ==========================================

python -m pip install --upgrade pip

pip install -r requirements.txt

pyinstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --windowed ^
    --name ExtremeMessageAnimator ^
    app.py

echo.
echo Building installer...

iscc installer.iss

echo.
echo ==========================================
echo BUILD COMPLETE
echo ==========================================

pause
