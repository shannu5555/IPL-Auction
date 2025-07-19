pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/shannu5555/IPL-Auction.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Check Status') {
            steps {
                sh 'docker ps'
            }
        }
    }
}
