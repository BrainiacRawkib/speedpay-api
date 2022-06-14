pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh "pip3 install --upgrade pip"
                sh "pip install -r requirements.txt"
            }
        }
        stage('Test') {
            steps {
                sh 'echo "Testing"'
            }
        }
        stage('Deploy') {
            steps {
                sh 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null jenkins@jenkins-server ubuntu@100.24.53.222 \
                "cd speedpay-api; \
                source venv/bin/activate; \
                git pull origin develop; \
                pip3 install -r requirements.txt --no-warn-script-location; \
                deactivate"'
            }
        }
    }
}