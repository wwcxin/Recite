@echo off
chcp 65001 >nul
echo 开始格式化JSON文件...
echo.

python format_json.py

if %errorlevel% neq 0 (
    echo.
    echo 错误: 脚本执行失败
    pause
    exit /b %errorlevel%
)

echo.
echo 完成！
pause

