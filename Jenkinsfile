pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dc035cc7-90ac-4ef4-baf2-92e893a3ea8d'
        IMAGE_NAME = 'shannu255/ipl-auction'
        TAG = 'latest'
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

        stage('Cleanup Old Containers') {
            steps {
                sh '''
                    docker stop ipl-auction || true
                    docker rm ipl-auction || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name ipl-auction $IMAGE_NAME:$TAG'
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
            slackSend(channel: '#ci', message: "✅ Build and Deployment Success!")
        }
        failure {
            slackSend(channel: '#ci', message: "❌ Build or Deployment Failed!")
        }
    }
}

