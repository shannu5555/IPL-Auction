pipeline {
    agent any

    environment {
        // Optional: set this as a parameter in Jenkins job config or via env vars
        FIRST_RUN = "true"
        DJANGO_SUPERUSER_USERNAME = "admin"
        DJANGO_SUPERUSER_EMAIL = "admin@example.com"
        DJANGO_SUPERUSER_PASSWORD = "adminpass"
    }

    stages {
        stage('Build and Run Docker') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    env.CONTAINER_ID = sh(script: "docker ps -qf 'ancestor=ipl-web'", returnStdout: true).trim()
                    sh "docker exec -i ${env.CONTAINER_ID} python manage.py migrate"
                }
            }
        }

        stage('Create Superuser (first-time only)') {
            when {
                expression { return env.FIRST_RUN == 'true' }
            }
            steps {
                sh """
                    docker exec -i ${env.CONTAINER_ID} python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists():
    User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')
EOF
                """
            }
        }

        stage("Echo Container ID") {
            steps {
                echo "Container ID: ${env.CONTAINER_ID}"
            }
        }        
    }
}
