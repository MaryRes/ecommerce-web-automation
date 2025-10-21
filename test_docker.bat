@echo off
echo Building Docker image...
docker build -t qa-tests .

echo.
echo Running quick Docker test...
docker run --rm qa-tests python tests/test_docker_quick.py

echo.
echo If you see SUCCESS messages, Docker works! 🎉
pause