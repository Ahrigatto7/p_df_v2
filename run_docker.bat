
@echo off
echo 🐳 Docker QA 시스템 실행 중...

:: 현재 디렉토리 이동
cd /d %~dp0

:: .env 파일 존재 확인
IF NOT EXIST ".env" (
    echo ❗ .env 파일이 존재하지 않습니다. 설정 후 다시 실행하세요.
    pause
    exit /b
)

:: Docker 실행
docker-compose down
docker-compose up --build

pause
