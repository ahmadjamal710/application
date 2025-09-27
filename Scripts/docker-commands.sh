#! /bin/bash

# Build and push frontend image
cd ../Application/frontend
docker build -t ahmadjamal710/todo-frontend .
docker push ahmadjamal710/todo-frontend

# Build and push backend image
cd ../backend
docker build -t backend ahmadjamal710/todo-backend .
docker push backend ahmadjamal710/todo-backend

# Run the stack locally
docker run -d -p 3306:3306 -v ~/database-storage:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_USER=admin -e MYSQL_PASSWORD=123 -e MYSQL_DATABASE=todoapp --name database mysql:latest
docker run -d -p 8000:8000 -e DB_NAME=todoapp -e DB_USER=admin -e DB_PASSWORD=123 -e DB_HOST=172.17.0.2 -e DB_PORT=3306 -e DEBUG=True -e SECRET_KEY=test --name backend ahmadjamal710/todo-backend
docker run -d -p 8080:80 -e BACKEND_DNS=172.17.0.3 -e BACKEND_PORT=8000 --name frontend ahmadjamal710/todo-frontend