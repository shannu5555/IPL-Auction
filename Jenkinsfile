pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/shannu5555/ipl-auction.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Run Containers') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Verify') {
            steps {
                sh 'docker ps'
            }
        }
    }
}
