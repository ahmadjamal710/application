 Devops To-Do List Application with Kubernetes Deployment

A production-grade, Devops To-Do List application with automated Kubernetes deployment using Jenkins CI/CD pipeline.

## Project Overview

This project consists of a 3-tier To-Do List application with the following components:

- Frontend: Static web application built with HTML, CSS, and JavaScript
- Backend: Django REST API application
- Database: MySQL database
- Infrastructure: Kubernetes deployment with CI/CD automation

## Architecture

The application is structured into three main components:

1. **Frontend**: Nginx-served static web application
2. **Backend**: Django REST API with health checks and authentication
3. **Database**: MySQL instance for data persistence

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python, Django, Django REST Framework
- **Database**: MySQL
- **CI/CD**: Jenkins with Kaniko for secure builds
- **Container Registry**: Docker Hub
- **Infrastructure**: Kubernetes
- **Load Balancing**: Nginx Ingress Controller
- **Storage**: AWS EBS CSI Driver

## Repository Structure

```
.
├── Application/
│   ├── frontend/          # Frontend static web application
│   │   ├── Dockerfile
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   └── backend/          # Django backend application
│       ├── Dockerfile
│       ├── apps/
│       └── todo_backend/
├── Manifests/           # Kubernetes manifests
│   ├── deployments.yaml
│   ├── services.yaml
│   └── volumes.yaml
├── Scripts/            # Utility scripts
│   ├── system-up.sh
│   └── docker-commands.sh
