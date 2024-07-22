pipeline {
    agent any

    environment {
        VENV_PATH = 'venv'
        FLASK_APP = 'workspace/flask/app.py'
        CHROME_DRIVER_PATH = "${WORKSPACE}/workspace/flask/chromedriver"
        PATH = "$VENV_PATH/bin:$CHROME_DRIVER_PATH:$PATH"
        SONARQUBE_SCANNER_HOME = tool name: 'SonarQube Scanner'
        SONARQUBE_TOKEN = 'squ_d5f444cca7aeeb9f3b05ed75a50f8c576a244eea'
        DEPENDENCY_CHECK_HOME = '/var/jenkins_home/tools/org.jenkinsci.plugins.DependencyCheck.tools.DependencyCheckInstallation/OWASP_Dependency-Check/dependency-check'
    }
    
    stages {
        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }
        
        stage('Clone Repository') {
            steps {
                dir('workspace') {
                    git branch: 'main', url: 'https://github.com/motorfireman/Test.git'
                }
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                dir('workspace/flask') {
                    sh 'python3 -m venv $VENV_PATH'
                }
            }
        }
        
        stage('Activate Virtual Environment and Install Dependencies') {
            steps {
                dir('workspace/flask') {
                    sh '. $VENV_PATH/bin/activate && pip install -r requirements.txt'
                }
            }
        }
        
        stage('Install Missing Libraries') {
            steps {
                sh '''
                apt-get update
                apt-get install -y libglib2.0-0 libnss3 libnssutil3 libnspr4
                '''
            }
        }
        
        stage('Dependency Check') {
            steps {
                script {
                    sh 'mkdir -p workspace/flask/dependency-check-report'
                    sh 'echo "Dependency Check Home: $DEPENDENCY_CHECK_HOME"'
                    sh 'ls -l $DEPENDENCY_CHECK_HOME/bin'
                    sh '${DEPENDENCY_CHECK_HOME}/bin/dependency-check.sh --project "Flask App" --scan . --format "ALL" --out workspace/flask/dependency-check-report || true'
                }
            }
        }
        
        stage('Download Chromedriver') {
            steps {
                script {
                    sh '''
                    curl -Lo chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
                    unzip -o chromedriver.zip -d workspace/flask
                    chmod +x workspace/flask/chromedriver
                    '''
                    sh 'ls -l workspace/flask/chromedriver' // Verify the chromedriver is downloaded correctly
                    sh 'ldd workspace/flask/chromedriver' // Check for missing dependencies
                    sh 'uname -m' // Print the system architecture
                }
            }
        }
        
        stage('UI Testing') {
            steps {
                script {
                    sh '. $VENV_PATH/bin/activate && FLASK_APP=$FLASK_APP flask run &'
                    sh 'sleep 5'
                    sh 'curl -s http://127.0.0.1:5000 || echo "Flask app did not start"'
                    sh 'curl -s -X POST -F "password=StrongPass123" http://127.0.0.1:5000 | grep "Welcome"'
                    sh 'curl -s -X POST -F "password=password" http://127.0.0.1:5000 | grep "Password does not meet the requirements"'
                    sh 'pkill -f "flask run"'
                }
            }
        }
        
        stage('Integration Testing') {
            steps {
                dir('workspace/flask') {
                    sh '. $VENV_PATH/bin/activate && pytest --junitxml=integration-test-results.xml'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('workspace/flask') {
                    sh 'docker build -t flask-app .'
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    dir('workspace/flask') {
                        sh '''
                        ${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=flask-app \
                        -Dsonar.sources=. \
                        -Dsonar.inclusions=app.py \
                        -Dsonar.host.url=http://sonarqube:9000 \
                        -Dsonar.login=${SONARQUBE_TOKEN}
                        '''
                    }
                }
            }
        }
        
        stage('Deploy Flask App') {
            steps {
                script {
                    echo 'Deploying Flask App...'
                    sh 'docker ps --filter publish=5000 --format "{{.ID}}" | xargs -r docker stop'
                    sh 'docker ps -a --filter status=exited --filter publish=5000 --format "{{.ID}}" | xargs -r docker rm'
                    sh 'docker run -d -p 5000:5000 flask-app'
                    sh 'sleep 10'
                }
            }
        }
        
        stage('Selenium Testing') {
            steps {
                dir('workspace/flask') {
                    sh '. $VENV_PATH/bin/activate && python selenium_test.py'
                }
            }
        }
    }
    
    post {
        failure {
            script {
                echo 'Build failed, not deploying Flask app.'
            }
        }
        always {
            archiveArtifacts artifacts: 'workspace/flask/dependency-check-report/*.*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'workspace/flask/integration-test-results.xml', allowEmptyArchive: true
        }
    }
}
