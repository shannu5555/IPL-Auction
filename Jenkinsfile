pipeline {
    agent any

    stages {
        stage('Build and Run Docker') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    def container_id = sh(script: "docker ps -qf 'ancestor=ipl-web'", returnStdout: true).trim()
                    sh "docker exec -i ${container_id} python manage.py migrate"
                }
            }
        }

        stage('Create Superuser (first-time only)') {
            when {
                expression { return env.FIRST_RUN == 'true' } // Set this variable in Jenkins if needed
            }
            steps {
                script {
                    def container_id = sh(script: "docker ps -qf 'ancestor=ipl-web'", returnStdout: true).trim()
                    sh """
                        docker exec -i ${container_id} python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
EOF
                    """
                }
            }
        }
        stage("echo output"){
            steps{
                echo "output"
            }
        }        
    }
}
