@echo off
echo 🚀 Cambridge Exam System - Automatic 502 Fix
echo ============================================

echo 📤 Transferring auto-fix script to VPS...
scp -P 22 -o StrictHostKeyChecking=no auto_fix_502.sh root@82.25.93.227:/tmp/

if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to transfer script. Please check your connection.
    pause
    exit /b 1
)

echo ✅ Script transferred successfully!
echo 🔧 Running auto-fix on VPS...
echo.

ssh -o StrictHostKeyChecking=no root@82.25.93.227 "chmod +x /tmp/auto_fix_502.sh && /tmp/auto_fix_502.sh"

if %ERRORLEVEL% equ 0 (
    echo.
    echo 🎉 AUTO-FIX COMPLETED SUCCESSFULLY!
    echo.
    echo Your Cambridge Exam System should now be accessible at:
    echo 👉 https://cambridgeexam.dobeda.com/
    echo.
    echo Testing the website...
    timeout /t 3 >nul
    start https://cambridgeexam.dobeda.com/
) else (
    echo.
    echo ⚠️ Auto-fix encountered some issues.
    echo Please check the output above for details.
)

echo.
echo Press any key to exit...
pause >nul