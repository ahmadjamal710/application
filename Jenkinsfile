pipeline {
    environment {
        DOCKER_IMAGE_FRONTEND = "ahmadjamal710/todo-frontend:v1.${env.BUILD_NUMBER}"
        DOCKER_IMAGE_BACKEND = "ahmadjamal710/todo-backend:v1.${env.BUILD_NUMBER}"
    }

    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  name: kaniko
  namespace: jenkins
spec:
  containers:
    - name: kaniko
      imagePullPolicy: IfNotPresent
      image: gcr.io/kaniko-project/executor:debug
      env:
        - name: DOCKER_CONFIG
          value: /kaniko/.docker
      command:
        - /busybox/cat
      tty: true
      volumeMounts:
        - name: docker-config
          mountPath: /kaniko/.docker
    - name: kubectl
      image: ubuntu:22.04
      command: ["/bin/sh", "-c"]
      args: ["sleep 9999"]
      tty: true
  volumes:
    - name: docker-config
      secret:
        secretName: dockerhub-secret
        items:
          - key: .dockerconfigjson
            path: config.json
  restartPolicy: Never
"""
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/ahmadjamal710/application.git']])
            }
        }
        
        stage('Frontend Build') {
            steps {
                container('kaniko') {
                    script {
                        sh """
                        /kaniko/executor --dockerfile `pwd`/Application/frontend/Dockerfile \
                                         --context `pwd`/Application/frontend \
                                         --destination=${DOCKER_IMAGE_FRONTEND}
                        """
                    }
                }
            }
        }
        
        stage('Backend Build') {
            steps {
                container('kaniko') {
                    script {
                        sh """
                        /kaniko/executor --dockerfile `pwd`/Application/backend/Dockerfile \
                                         --context `pwd`/Application/backend \
                                         --destination=${DOCKER_IMAGE_BACKEND}
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                container('kubectl') {
                    sh '''
                        apt-get update -qq
                        apt-get install -y -qq curl apt-transport-https gpg

                        # Add the new repo
                        curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | gpg --dearmor -o /etc/apt/trusted.gpg.d/kubernetes.gpg
                        echo "deb [signed-by=/etc/apt/trusted.gpg.d/kubernetes.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /" > /etc/apt/sources.list.d/kubernetes.list

                        apt-get update -qq
                        apt-get install -y -qq kubectl

                        echo "Kubectl installed via apt:"
                        kubectl version --client
                        
                        cd Manifests
                        sed -i -E "s|(image: ahmadjamal710/todo-frontend):[a-zA-Z0-9._-]+|\\1:v1.${BUILD_NUMBER}|g" deployments.yaml
                        sed -i -E "s|(image: ahmadjamal710/todo-backend):[a-zA-Z0-9._-]+|\\1:v1.${BUILD_NUMBER}|g" deployments.yaml
                        kubectl apply -f deployments.yaml
                    '''
                }
            }
        }
    }
}