pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url:'https://github.com/shannu5555/IPL-Auction.git'
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

        stage('Run Migrations') {
            steps {
                sh 'docker-compose exec web python manage.py migrate'
            }
        }

        stage('Check Status') {
            steps {
                sh 'docker ps'
            }
        }
    }
}

