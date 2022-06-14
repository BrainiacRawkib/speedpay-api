pipeline {
    agent {label "linux"}
    stages {
        stage('Build') {
            steps {
                sh "pip install --upgrade pip"
                sh "pip install requirements.txt"
            }
        }
        stage('Test') {
            steps {
                echo "Testing"
            }
        }
        stage('Deploy') {
            steps {
                sh 'ssh ubuntu@100.24.53.222 \
                "cd speedpay-api; \
                source venv/bin/activate; \
                git pull origin develop; \
                pip install -r requirements.txt --no-warn-script-location "'
            }
        }
    }
}