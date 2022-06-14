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
        stage('Deploy to main server') {
            input {
                message "Deploy to live server"
                ok "Yes"
            }
            steps {
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@52.207.255.6 "cd speedpay-api; \
                source venv/bin/activate; \
                git pull origin main; \
                pip3 install -r requirements.txt --no-warn-script-location; \
                deactivate "'
            }
            
        }
    }
}