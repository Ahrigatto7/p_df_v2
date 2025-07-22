
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
set COMPOSE_FILE=docker-compose-postgres.yml
IF NOT EXIST "%COMPOSE_FILE%" (
    echo ❗ %COMPOSE_FILE% 파일을 찾을 수 없습니다.
    pause
    exit /b
)
docker-compose -f %COMPOSE_FILE% down
docker-compose -f %COMPOSE_FILE% up --build

pause
