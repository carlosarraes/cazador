pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'carlosarraes/cazadorpy'
        DOCKER_TAG = 'latest'
        REPO_URL = 'https://github.com/carlosarraes/cazadorpy.git'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning...'
                sh "git clone ${REPO_URL}"
            }
        }
        stage('Build docker images') {
            steps {
                echo 'Building...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes(Minikube)..'
                sh "kubectl apply -f k8s/"
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution complete.'
        }
    }
}
