pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = '3bbfe990-08d3-43b5-85d4-172db056b333'
        IMAGE_NAME = 'shannu255/ipl-auction'
        TAG = 'latest'
        CONTAINER_NAME = 'ipl-auction'
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/shannu5555/IPL-Auction.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$TAG .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh 'docker push $IMAGE_NAME:$TAG'
            }
        }

        stage('Run Migrations') {
            steps {
                sh 'docker run --rm $IMAGE_NAME:$TAG sh -c "python manage.py migrate"'
            }
        }


        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME:$TAG'
            }
        }

        stage('Check Status') {
            steps {
                sh 'docker ps'
            }
        }
    }

    post {
        success {
            echo "✅ Build and Deployment Success!"
        }
        failure {
            echo "❌ Build or Deployment Failed!"
        }
    }
}




