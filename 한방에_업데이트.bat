@echo off
chcp 65001 > lul
echo [1/2] 데이터 동기화 중...
python c:\ys_start\GE\update_all.py

echo.
echo [2/2] 실행 파일(EXE) 재빌드 중... (시간이 조금 걸립니다)
pyinstaller --noconfirm c:\ys_start\GE\SecurityQuiz_Ultimate_v3.spec

echo.
echo ==========================================
echo 모든 업데이트가 완료되었습니다!
echo 이제 dist 폴더의 EXE와 web 폴더를 확인하세요.
echo ==========================================
pause
