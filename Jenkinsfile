pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh "echo 'pip install --upgrade pip'"
                sh "echo 'pip install requirements.txt'"
            }
        }
        stage('Test') {
            steps {
                sh 'echo "Testing"'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo "welcome"'
            }
        }
    }
}