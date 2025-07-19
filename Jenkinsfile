pipeline {
    agent any

    environment {
        IMAGE_NAME = 'shannu255/ipl-auction:latest'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/shannu255/ipl-auction.git',
                        credentialsId: '3bbfe990-08d3-43b5-85d4-172db056b333'  // Replace with your Jenkins credential ID
                    ]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Cleanup Old Container') {
            steps {
                sh '''
                    CONTAINER_ID=$(docker ps -q --filter "publish=8000")
                    if [ ! -z "$CONTAINER_ID" ]; then
                        echo "Stopping existing container using port 8000: $CONTAINER_ID"
                        docker stop $CONTAINER_ID
                        docker rm $CONTAINER_ID
                    else
                        echo "No running container found using port 8000"
                    fi
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name ipl-auction $IMAGE_NAME'
            }
        }
    }

    post {
        success {
            slackSend(channel: '#ci', message: "✅ Build Success for *${env.JOB_NAME}* (#${env.BUILD_NUMBER})")
        }
        failure {
            slackSend(channel: '#ci', message: "❌ Build Failed for *${env.JOB_NAME}* (#${env.BUILD_NUMBER})")
        }
    }
}



