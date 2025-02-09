# docker run -p 5000:5000 budget-manager-app:slim
docker run -p 5000:5000 -w /app -v "$(pwd):/app" budget-manager-app:slim
