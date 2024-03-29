pipeline {
    agent { label 'ec2-agent'}

    environment {
        DOCKER_IMAGE = 'devrico003/ha-jenkins-11-02-24'
        IMAGE_TAG = 'latest'
        TEST_SERVER = '3.120.40.159'
        TEST_SERVER_USER = 'ubuntu'
        TEST_CONTAINER_NAME = 'ha-jenkins-11-02-24'
    }

    stages {
        stage('Clone repository') {
                    steps {
                        echo 'Start: Cloning repository...'
                        checkout scm: [$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[credentialsId: 'github-id', url: 'https://github.com/DevRico003/ha-jenkins-11-02-24.git']]]
                        echo 'End: Repository cloned.'
                    }
                }

        stage('Setup Virtual Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }


        stage('Code Quality Analysis') {
            steps {
                sh script: '''
                    . venv/bin/activate
                    pylint app.py
                    result=$?
                    if [ "$result" -eq 1 ]; then
                        echo "Pylint found errors that prevent the pipeline from continuing."
                        exit 1
                    fi
                    ''', returnStatus: true

            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to Test Server with Ansible') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'ssh-key', keyFileVariable: 'sshPrivateKey')]) {
                        ansiblePlaybook(
                            playbook: 'deploy_app.yml',
                            inventory: 'hosts.ini',
                            extras: "-e ansible_ssh_private_key_file=${sshPrivateKey} -e DOCKER_IMAGE=${DOCKER_IMAGE} -e IMAGE_TAG=${IMAGE_TAG} -e TEST_CONTAINER_NAME=${TEST_CONTAINER_NAME}"
                        )
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'The pipeline completed successfully.'
        }
        failure {
            echo 'The pipeline failed.'
        }
    }
}
