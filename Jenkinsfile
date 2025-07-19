pipeline {
    agent any

    environment {
        // You can also inject these from Jenkins Credentials for better security
        FIRST_RUN = "true"
        DJANGO_SUPERUSER_USERNAME = "admin"
        DJANGO_SUPERUSER_EMAIL = "admin@example.com"
        DJANGO_SUPERUSER_PASSWORD = "adminpass"
    }

    stages {
        stage('Build and Run Docker') {
            steps {
                echo '📦 Building and starting Docker container...'
                sh 'docker-compose up -d --build'
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    echo '🔄 Applying Django migrations...'
                    env.CONTAINER_ID = sh(script: "docker ps -qf 'ancestor=ipl-web'", returnStdout: true).trim()
                    sh "docker exec -i ${env.CONTAINER_ID} python manage.py migrate"
                }
            }
        }
        
        stage('Create Superuser') {
            when {
                expression { return env.FIRST_RUN == 'true' } // Only run on first build
            }
            steps {
                script {
                    echo '👤 Creating Django superuser (if not exists)...'
                    def container_id = sh(script: "docker ps -qf 'ancestor=ipl-web'", returnStdout: true).trim()

                    sh """
                        docker exec -e DJANGO_SUPERUSER_USERNAME=${env.DJANGO_SUPERUSER_USERNAME} \\
                                     -e DJANGO_SUPERUSER_EMAIL=${env.DJANGO_SUPERUSER_EMAIL} \\
                                     -e DJANGO_SUPERUSER_PASSWORD=${env.DJANGO_SUPERUSER_PASSWORD} \\
                                     ${container_id} sh -c 'python manage.py shell < create_superuser.py'
                    """
                }
            }
        }

        stage('Done') {
            steps {
                echo "✅ Pipeline completed successfully."
                echo "ℹ️  Container ID used: ${env.CONTAINER_ID}"
            }
        }
    }
}

